from mininet.log import setLogLevel
from mn_wifi.net import Mininet_wifi
from mn_wifi.node import UserAP
from mn_wifi.cli import CLI
import time

def get_bssid(sta):
    """Return the BSSID (MAC address) of the AP sta is currently associated with."""
    output = sta.cmd('iw dev %s-wlan0 link' % sta.name)
    for line in output.splitlines():
        if 'Connected to' in line:
            return line.split()[2]
    return None

def topology():
    net = Mininet_wifi(accessPoint=UserAP)
    net.setPropagationModel(model="logDistance", exp=4.5)

    print("*** Creating nodes")
    ap1 = net.addAccessPoint('ap1', ssid='ssid1', mode='g', channel='1', position='10,30,0', txpower=15, mac='00:00:00:00:00:01')
    ap2 = net.addAccessPoint('ap2', ssid='ssid2', mode='g', channel='6', position='50,30,0', txpower=15, mac='00:00:00:00:00:02')
    sta1 = net.addStation('sta1', position='12,30,0')
    c1 = net.addController('c1')

    print("*** Configuring WiFi nodes")
    net.configureWifiNodes()

    print("*** Starting network")
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])

    log = []
    time.sleep(5)

    ap2_mac = ap2.params['mac']
    initial_bssid = get_bssid(sta1)
    log.append((time.time(), f"Initial BSSID: {initial_bssid}"))

    handover_time = None

    for tx in [10, 5, 2, 1, 0]:
        ap1.setTxPower(tx)
        time.sleep(3)
        bssid = get_bssid(sta1)
        log.append((time.time(), f"AP1 txpower {tx} dBm, sta1 BSSID: {bssid}"))

        if bssid and ap2_mac.lower() in bssid.lower():
            handover_time = log[-1][0]
            log.append((handover_time, 'Handover to AP2 detected!'))
            break

    if not handover_time:
        print("*** Forcing handover by moving station closer to AP2")
        sta1.setPosition('48,30,0')
        time.sleep(5)
        sta1.cmd('iw dev sta1-wlan0 disconnect')
        time.sleep(2)
        sta1.cmd('iw dev sta1-wlan0 connect ssid2')
        time.sleep(5)
        bssid = get_bssid(sta1)
        log.append((time.time(), f"Moved sta1 near AP2, BSSID: {bssid}"))

        if bssid and ap2_mac.lower() in bssid.lower():
            handover_time = log[-1][0]
            log.append((handover_time, 'Handover to AP2 detected after movement!'))

    print("\n=== Handover Log ===")
    for t, msg in log:
        print(f"{time.strftime('%H:%M:%S', time.localtime(t))}: {msg}")

    if handover_time:
        print("\nHandover time: %.3f seconds" % (handover_time - log[0][0]))
    else:
        print("\nHandover did not occur.")

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()

