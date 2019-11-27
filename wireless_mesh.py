#!/usr/bin/python

"""This example shows how to work in adhoc mode

It is a full mesh network

     .sta3.
    .      .
   .        .
sta1 ----- sta2"""

import sys

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, mesh
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference


def topology(mobility):
    "Create a network."
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference, controller=Controller)

    info("*** Creating nodes\n")
    if mobility:
        host = net.addHost('host', position='90,90,0', mac='00:00:00:00:00:01', ip='10.0.0.1/8')
        sta1 = net.addStation('sta1', position='20,70,0', range=5)
        sta2 = net.addStation('sta2', position='50,70,0', range=5)
        sta3 = net.addStation('sta3', position='80,70,0', range=5)
        ap1 = net.addAccessPoint('ap1', wlans=2, ssid='ssid1,ssid12', position='35,60,0', range='30,30')
        ap2 = net.addAccessPoint('ap2', wlans=2, ssid='ssid2,ssid22', position='65,60,0', range='30,30')
        ap3 = net.addAccessPoint('ap3', wlans=2, ssid='ssid1,ssid12', position='25,30,0', range='20,20')
        ap4 = net.addAccessPoint('ap4', wlans=2, ssid='ssid2,ssid22', position='50,30,0', range='20,20')
        ap5 = net.addAccessPoint('ap5', wlans=2, ssid='ssid1,ssid12', position='75,30,0', range='20,20')
        c0 = net.addController('c0')

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=4)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")
    net.addLink(ap1, host, bw=10, delay='30ms')

    net.plotGraph(max_x=100, max_y=100)

    # if mobility:
    #     net.plotGraph(max_x=100, max_y=100)
    #     net.startMobility(time=0, model='RandomDirection',
    #                       max_x=100, max_y=100,
    #                       min_v=0.5, max_v=0.8, seed=20)

    info("*** Starting network\n")
    net.build()
    c0.start()
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
    setLogLevel('info')
    mobility = True if '-m' in sys.argv else False
    topology(mobility)

