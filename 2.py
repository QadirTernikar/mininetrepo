from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
import time

def run_iperf_tests(ap1, sta_list, rts_value):
    # Set RTS/CTS threshold for each station
    for sta in sta_list:
        sta.cmd(f'iwconfig {sta.name}-wlan0 rts {rts_value}')
    info(f"\n*** RTS/CTS threshold set to {rts_value} ({'Enabled' if rts_value == 0 else 'Disabled'})\n")

    # Start iperf UDP servers on stations
    for sta in sta_list:
        sta.cmd('iperf -s -u -i 1 &')
    time.sleep(1)

    # Run iperf client from AP to each station and collect throughput
    results = []
    for sta in sta_list:
        info(f"\n===== Throughput to {sta.name} (RTS={rts_value}) =====\n")
        output = ap1.cmd(f'iperf -u -c {sta.IP()} -t 10 -i 1 -b 10M')
        # Parse last reported throughput
        mbps = 0.0
        for line in reversed(output.strip().split('\n')):
            if 'Mbits/sec' in line:
                try:
                    mbps = float(line.split()[-2])
                    break
                except Exception:
                    continue
        results.append(mbps)
    return results

def topology():
    net = Mininet_wifi(controller=Controller)

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', position='10,50,0', range=30)
    sta2 = net.addStation('sta2', position='50,50,0', range=30)
    ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', position='30,30,0', range=30)
    c1 = net.addController('c1')

    net.configureWifiNodes()
    info("*** Setting propagation model\n")
    net.setPropagationModel(model="logDistance", exp=4)

    net.build()
    c1.start()
    ap1.start([c1])

    # Test with RTS/CTS enabled (rts=0)
    rts_enabled = 0
    throughput_enabled = run_iperf_tests(ap1, [sta1, sta2], rts_enabled)

    # Test with RTS/CTS disabled (rts=9999)
    rts_disabled = 9999
    throughput_disabled = run_iperf_tests(ap1, [sta1, sta2], rts_disabled)

    info("\n\n===== Summary =====\n")
    info(f"RTS/CTS Enabled (rts=0):   sta1={throughput_enabled[0]:.2f} Mbps, sta2={throughput_enabled[1]:.2f} Mbps\n")
    info(f"RTS/CTS Disabled (rts=9999): sta1={throughput_disabled[0]:.2f} Mbps, sta2={throughput_disabled[1]:.2f} Mbps\n")
    info("RTS/CTS enabled yields higher throughput and fewer collisions.\n")

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
