#!/usr/bin/python3

from mininet.node import Controller
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from time import sleep
import os

def topology():
    net = Mininet_wifi(controller=Controller)

    print("*** Creating nodes")
    sta1 = net.addStation('sta1', position='10,20,0')
    h1 = net.addHost('h1', ip='10.0.0.100')
    ap1 = net.addAccessPoint('ap1', ssid='ap1-ssid', mode='g', channel='1', position='15,20,0')
    ap2 = net.addAccessPoint('ap2', ssid='ap2-ssid', mode='g', channel='6', position='80,20,0')
    c0 = net.addController('c0')

    print("*** Configuring WiFi nodes")
    net.configureWifiNodes()

    net.addLink(ap1, h1)
    net.addLink(ap2, h1)

    print("*** Starting network")
    net.build()
    c0.start()
    ap1.start([c0])
    ap2.start([c0])

    print("*** Starting UDP video stream on h1 using VLC")
    # Requires sample.mp4 in home directory
    h1.cmd('cvlc --intf dummy ~/sample.mp4 --loop --sout "#duplicate{dst=udp{dst=10.0.0.1:1234}}" > /tmp/vlc.log 2>&1 &')
    sleep(3)

    print("*** Starting ffplay video player on sta1")
    sta1.cmd('xterm -hold -e ffplay -fflags nobuffer -loglevel quiet udp://@:1234 &')
    sleep(2)

    print("*** Start ping to monitor connectivity")
    sta1.cmd('xterm -hold -e ping 10.0.0.100 > /tmp/ping_log.txt &')

    print("*** Log initial connection info")
    print(sta1.cmd('iw dev sta1-wlan0 link'))

    print("*** Waiting before moving...")
    sleep(5)

    print("*** Moving sta1 towards AP2 (handover happens here)")
    sta1.setPosition('85,20,0')
    sleep(15)

    print("*** Log post-handover connection info")
    print(sta1.cmd('iw dev sta1-wlan0 link'))

    print("*** Open CLI to allow manual observation")
    CLI(net)

    print("*** Dumping logs for analysis")
    print("\n--- VLC Log ---")
    os.system('cat /tmp/vlc.log')

    print("\n--- Ping Log ---")
    os.system('cat /tmp/ping_log.txt')

    print("*** Stopping network")
    net.stop()

if __name__ == '__main__':
    topology()

