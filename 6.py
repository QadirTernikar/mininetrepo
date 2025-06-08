#!/usr/bin/python3

from mn_wifi.net import Mininet_wifi
from mininet.node import Controller
from time import sleep

def topology():
    net = Mininet_wifi(controller=Controller)

    print("*** Creating nodes")
    sta1 = net.addStation('sta1', position='50,20,0')
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

    print("*** Connecting sta1 to AP2")
    sta1.cmd('iw dev sta1-wlan0 connect ap2-ssid')
    sleep(5)
    print(sta1.cmd('iw dev sta1-wlan0 link'))

    print("*** Opening xterm and starting ping to h1")
    sta1.cmd('xterm -hold -e ping -c 30 10.0.0.100 &')
    sleep(5)

    print("*** Moving sta1 towards AP1")
    sta1.setPosition('15,20,0')
    sleep(5)

    print("*** Disconnecting from AP2")
    sta1.cmd('iw dev sta1-wlan0 disconnect')
    sleep(6)

    print("*** Connecting to AP1")
    sta1.cmd('iw dev sta1-wlan0 connect ap1-ssid')
    sleep(5)
    print(sta1.cmd('iw dev sta1-wlan0 link'))
    sleep(10)

    print("*** Stopping network")
    net.stop()

if __name__ == '__main__':
    topology()

