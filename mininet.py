from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSController, RemoteController, CPULimitedHost
from mininet.link import TCLink
from mininet.nodelib import NAT
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
import time

# GUI Tkinter packages
import Tkinter as tk
from Tkinter import *
import tkMessageBox

class ProjTopo(Topo):

	def build(self, h = 1):

		gatewayIP = '10.0.1.254' # establish a default gateway

		# create NAT node for network
		nat = self.addNode('nat', cls=NAT, ip=gatewayIP, inNamespace=False)

		# edge switch to connect with NAT node
		s1 = self.addSwitch('s1', dpid = "00:00:00:00:00:00:00:01")
		self.addLink(s1, nat, port1=1, port2=1)


		# consumer edge switch to connect to host
		s2 = self.addSwitch('s2', dpid = "00:00:00:00:00:00:00:02")
		# connect consumer switch to NAT switch
		self.addLink(s1, s2, port1=2, port2=2, bw=50) # generic link
		self.addLink(s1, s2, port1=3, port2=3, bw=200) # high bandwidth link

		# connect consumer switch to host
		host = self.addHost('h1', ip='10.0.1.1', defaultRoute='via %s' % gatewayIP) # TODO: figure out what defaultRoute argument means
		self.addLink(s2, host, cls = TCLink, port1=1)


def GUI():
	root = tk.Tk()
	root.title("Flow tables of network switches")
	root.geometry("%dx%d+50+30" % (650,650))
	height = 5
	width = 5
	for i in range(height): #Rows
		for j in range(width): #Columns
			b = Entry(root, text="row: %d, column: %d" % (i, j))
			b.grid(row=i, column=j)

def simpleTest():

	topo = ProjTopo()
	natSubnet = '10.0.0.0/23'
	net = Mininet(topo=topo, controller=None, autoSetMacs=True, autoStaticArp=True,ipBase=natSubnet)
	net.addController('c0', controller=RemoteController, ip="127.0.0.1", port=6633, protocols="OpenFlow13")
	net.start()

	CLI(net)

	GUI()

	# while(1):

	# 	s1_flows = net.switches[0].cmd('ovs-ofctl dump-flows s1')
	# 	s2_flows = net.switches[1].cmd('ovs-ofctl dump-flows s2')

	# 	print(s1_flows)
	# 	print(s2_flows)

	# 	time.sleep(5)



	net.stop()

topos = { 'mytopo': (lambda: simpleTest() ) }