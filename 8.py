#!/usr/bin/python3
from mininet.cli import CLI
from mn_wifi.net import Mininet_wifi
from mininet.node import Controller
from time import sleep

def topology():
    net = Mininet_wifi(controller=Controller)

    print("*** Creating nodes")
    sta1 = net.addStation('sta1', position='15,20,0')
    h1 = net.addHost('h1', ip='10.0.0.100')
    s1 = net.addSwitch('s1')
    ap1 = net.addAccessPoint('ap1', ssid='ap1-ssid', mode='g', channel='1', position='15,20,0')
    ap2 = net.addAccessPoint('ap2', ssid='ap2-ssid', mode='g', channel='6', position='55,20,0')
    c0 = net.addController('c0')

    net.configureWifiNodes()

    net.addLink(ap1, s1)
    net.addLink(ap2, s1)
    net.addLink(h1, s1)

    net.build()
    c0.start()
    s1.start([c0])
    ap1.start([c0])
    ap2.start([c0])

    print("*** Connecting sta1 to AP1")
    sta1.cmd('iw dev sta1-wlan0 connect ap1-ssid')
    sleep(5)

    print("*** Starting UDP iperf server on h1")
    h1.cmd('iperf -s -u -i 1 > /tmp/iperf_server.log &')
    sleep(2)

    print("*** Starting UDP iperf client on sta1")
    sta1.cmd('iperf -c 10.0.0.100 -u -t 30 -b 10M -i 1 > /tmp/iperf_client.log &')
    sleep(10)

    print("*** Moving sta1 to AP2")
    sta1.setPosition('55,20,0')
    sleep(10)

    print("*** Stopping iperf")
    sta1.cmd('kill %iperf')
    h1.cmd('kill %iperf')

    print("\n*** iperf server log (/tmp/iperf_server.log):\n")
    print(h1.cmd('cat /tmp/iperf_server.log'))


    CLI(net)
    net.stop()

if __name__ == '__main__':
    topology()

