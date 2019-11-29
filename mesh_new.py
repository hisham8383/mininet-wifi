#!/usr/bin/python

import sys

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mininet.link import Intf
from mn_wifi.link import wmediumd, mesh
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
from mininet.nodelib import LinuxBridge


def topology():
    "Create a network."
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference, controller=Controller)

    info("*** Creating nodes\n")

    # TODO should we put a compute node next to each AP?

    cloud = net.addHost('cloud')
    host  = net.addHost('host') 
    s6    = net.addSwitch('s6') # make sure the number of the switch does not overlap with the numbers of APs

    sta1 = net.addStation('sta1', range=5, ip='10.0.0.201/8')
    sta2 = net.addStation('sta2', range=5, ip='10.0.0.202/8')
    sta3 = net.addStation('sta3', range=5, ip='10.0.0.203/8')

    ap1 = net.addAccessPoint('ap1', wlans=2, ssid='ssid00,ssid01', position='35,60,0', range='40,40', ip='10.0.0.101/8')
    ap2 = net.addAccessPoint('ap2', wlans=2, ssid='ssid10,ssid11', position='65,60,0', range='40,40', ip='10.0.0.102/8')
    ap3 = net.addAccessPoint('ap3', wlans=2, ssid='ssid20,ssid21', position='25,30,0', range='30,30', ip='10.0.0.103/8')
    ap4 = net.addAccessPoint('ap4', wlans=2, ssid='ssid30,ssid31', position='50,30,0', range='30,30', ip='10.0.0.104/8')
    ap5 = net.addAccessPoint('ap5', wlans=2, ssid='ssid40,ssid41', position='75,30,0', range='30,30', ip='10.0.0.105/8')

    c0 = net.addController('c0')

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=4)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Associating Stations\n")

    net.addLink(s6, host,  bw=54, delay='30ms')  # fast local link
    net.addLink(s6, ap1,   bw=54, delay='30ms')  # fast local link
    net.addLink(s6, cloud, bw=6,  delay='130ms') # less reliable Internet connection

    # create a mesh network out of the APs
    net.addLink(ap1, intf='ap1-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)
    net.addLink(ap2, intf='ap2-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)
    net.addLink(ap3, intf='ap3-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)
    net.addLink(ap4, intf='ap4-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)
    net.addLink(ap5, intf='ap5-wlan2', cls=mesh, ssid='mesh-ssid', channel=5)

    net.plotGraph(min_x=0, min_y=0, max_x=110, max_y=110)
    net.startMobility(time=0, model='RandomDirection', min_x=5,
                          max_x=90, min_y=10, max_y=90,
                          min_v=0.5, max_v=0.8, seed=20)
    info("*** Starting network\n")
    net.build()
    c0.start()
    s6.start([c0])
    ap1.start([c0])
    ap2.start([c0])
    ap3.start([c0])
    ap4.start([c0])
    ap5.start([c0])

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    #setLogLevel('info')
    topology()
