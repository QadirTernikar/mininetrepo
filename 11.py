from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference

def topology():
    net = Mininet_wifi(controller=Controller, link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', ip='10.0.0.1/8', position='10,50,0')
    ap1 = net.addAccessPoint('ap1', ssid='ap1-ssid', mode='g', channel='1', position='30,50,0', range=20)
    ap2 = net.addAccessPoint('ap2', ssid='ap2-ssid', mode='g', channel='6', position='60,50,0', range=20)
    ap3 = net.addAccessPoint('ap3', ssid='ap3-ssid', mode='g', channel='11', position='90,50,0', range=20)
    c1 = net.addController('c1')

    net.configureWifiNodes()

    info("*** Associating and Creating links\n")
    net.plotGraph(max_x=120, max_y=100)
    net.startMobility(time=0)
    net.mobility(sta1, 'start', time=1, position='10,50,0')
    net.mobility(sta1, 'stop', time=30, position='100,50,0')
    net.stopMobility(time=31)

    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])
    ap3.start([c1])

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()

