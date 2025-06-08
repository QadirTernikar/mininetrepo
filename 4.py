from mininet.node import Controller
from mininet.log import setLogLevel
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
from time import sleep

def topology():
    net = Mininet_wifi(controller=Controller, link=wmediumd, wmediumd_mode=interference)

    print("*** Creating nodes")
    sta1 = net.addStation('sta1', position='10,30,0')
    sta2 = net.addStation('sta2', position='15,30,0')
    sta3 = net.addStation('sta3', position='20,30,0')
    sta4 = net.addStation('sta4', position='25,30,0')
    sta5 = net.addStation('sta5', position='30,30,0')
    ap1 = net.addAccessPoint('ap1', ssid='wifi', mode='g', channel='1', position='40,30,0')
    c1 = net.addController('c1')

    print("*** Configuring wifi nodes")
    net.configureWifiNodes()

    print("*** Starting network")
    net.build()
    c1.start()
    ap1.start([c1])

    # Start iperf UDP servers on each station
    print("*** Starting iperf UDP servers")
    for sta in [sta1, sta2, sta3, sta4, sta5]:
        sta.cmd('iperf -s -u &')
    sleep(1)

    print("\n*** Running UDP iperf clients from AP to each station\n")

    print("\n===== Throughput to sta1 =====")
    ap1.cmdPrint(f'iperf -u -c {sta1.IP()} -t 10 -i 1 -b 10M -l 512')

    print("\n===== Throughput to sta2 =====")
    ap1.cmdPrint(f'iperf -u -c {sta2.IP()} -t 10 -i 1 -b 10M -l 512')

    print("\n===== Throughput to sta3 =====")
    ap1.cmdPrint(f'iperf -u -c {sta3.IP()} -t 10 -i 1 -b 10M -l 512')

    print("\n===== Throughput to sta4 =====")
    ap1.cmdPrint(f'iperf -u -c {sta4.IP()} -t 10 -i 1 -b 10M -l 512')

    print("\n===== Throughput to sta5 =====")
    ap1.cmdPrint(f'iperf -u -c {sta5.IP()} -t 10 -i 1 -b 10M -l 512')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
