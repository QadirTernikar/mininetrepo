from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
import time

def run_iperf_tests(ap1, sta_list):
    # Start iperf UDP servers on stations
    for sta in sta_list:
        sta.cmd('iperf -s -u -i 1 &')
    time.sleep(1)

    results = []
    for sta in sta_list:
        info(f"\n===== Throughput to {sta.name} =====\n")
        output = ap1.cmd(f'iperf -u -c {sta.IP()} -t 10 -i 1 -b 30M')
        mbps = 0.0
        for line in reversed(output.strip().split('\n')):
            if 'Mbits/sec' in line:
                try:
                    mbps = float(line.split()[-2])
                    break
                except Exception:
                    continue
        info(f"{sta.name} throughput: {mbps:.2f} Mbps\n")
        results.append(mbps)
    return results

def topology():
    net = Mininet_wifi(controller=Controller)

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', position='10,30,0')     # Near AP
    sta2 = net.addStation('sta2', position='1000000,30000,0')    # Far from AP
    ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', mode='g', channel='1', position='50,30,0')
    c1 = net.addController('c1')

    info("*** Configuring WiFi nodes\n")
    net.setPropagationModel(model="logDistance", exp=4)  # Use path loss model
    net.configureWifiNodes()

    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])

    info("*** Running iperf tests from AP to sta1 (near) and sta2 (far)\n")
    throughput = run_iperf_tests(ap1, [sta1, sta2])

    info("\n===== Summary =====\n")
    info(f"sta1 (near):   {throughput[0]:.2f} Mbps (higher, stable throughput)\n")
    info(f"sta2 (far):    {throughput[1]:.2f} Mbps (degraded throughput due to lower SNR and increased packet loss)\n")

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
