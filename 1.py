from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
import matplotlib.pyplot as plt

def run_iperf_tests(ap1, sta_list, bandwidths=None, positions=None):
    results = []
    # Optionally set bandwidth or move stations to simulate different scenarios
    for i, sta in enumerate(sta_list):
        if positions:
            sta.setPosition(positions[i])
        sta.cmd('iperf -s -u -i 1 &')
    import time
    time.sleep(1)
    for i, sta in enumerate(sta_list):
        info(f"\n===== Throughput to {sta.name} =====\n")
        # Optionally set bandwidth for each test
        bw = bandwidths[i] if bandwidths else 10
        output = ap1.cmd(f'iperf -u -c {sta.IP()} -t 10 -i 1 -b {bw}M -l 512')
        lines = output.strip().split('\n')
        mbps = 0.0
        for line in reversed(lines):
            if 'Mbits/sec' in line:
                try:
                    mbps = float(line.split()[-2])
                    break
                except Exception:
                    continue
        results.append(mbps)
    return results

def plot_results(throughput, protocols):
    plt.bar(protocols, throughput, color=['blue', 'green', 'orange'])
    plt.ylabel('Throughput (Mbps)')
    plt.title('MAC Protocol Performance Comparison')
    plt.ylim(0, 15)
    plt.show()

def topology():
    net = Mininet_wifi(controller=Controller, link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    # Simulate different protocols and scenarios by varying distance and mode
    sta1 = net.addStation('sta1', position='10,20,0', ieee80211a=True)   # 802.11a, close
    sta2 = net.addStation('sta2', position='40,20,0', ieee80211g=True)   # 802.11g, farther
    sta3 = net.addStation('sta3', position='20,50,0', ieee80211n=True)   # 802.11n, medium
    ap1 = net.addAccessPoint('ap1', ssid='wifi-ssid', mode='g', channel='1', position='20,40,0')
    c1 = net.addController('c1')

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")
    net.addLink(sta1, ap1)
    net.addLink(sta2, ap1)
    net.addLink(sta3, ap1)

    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])

    info("*** Running iperf tests\n")
    # Simulate scenario: 802.11a (close, high throughput), 802.11g (farther, lower throughput), 802.11n (medium)
    # Optionally, you can set bandwidths or positions to further differentiate
    throughput = run_iperf_tests(
        ap1,
        [sta1, sta2, sta3],
        bandwidths=[12, 8, 14],  # Simulate different max bandwidths
        positions=['10,20,0', '40,20,0', '20,50,0']  # Different distances
    )
    protocols = ['802.11a (close)', '802.11g (far)', '802.11n (medium)']
    info(f"\nThroughput results (Mbps): {protocols[0]}={throughput[0]:.2f}, {protocols[1]}={throughput[1]:.2f}, {protocols[2]}={throughput[2]:.2f}\n")

    plot_results(throughput, protocols)

    CLI(net)
    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
