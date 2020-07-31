#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSController, RemoteController, CPULimitedHost
from mininet.link import TCLink
from mininet.nodelib import NAT
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI

# GUI Tkinter packages
import Tkinter as tk
from Tkinter import *
import tkMessageBox

# root = tk.Tk()
# s1_lbl = Label(root, text='0')
# s2_lbl = Label(root, text='0')

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


def GUI(net):
    root = tk.Tk()
    root.title("Flow tables of network switches")
    root.geometry("%dx%d+50+30" % (650,650))

    cv = tk.Canvas(width=650, height=650)
    # cv.pack(side='top', fill='both', expand='yes')
    cv.create_image(0, 0, anchor='nw')

    s1_flows = net.switches[0].cmd('ovs-ofctl dump-flows s1')
    s2_flows = net.switches[1].cmd('ovs-ofctl dump-flows s2')

    s1_lbl = Label(root, text=s1_flows)
    s2_lbl = Label(root, text=s2_flows)

    s1_lbl.grid(column=0,row=0)
    s2_lbl.grid(column=0,row=1)

    print(s1_flows)
    print(s2_flows)

    # height = 5
    # width = 5
    # for i in range(height): #Rows
    #     for j in range(width): #Columns
    #         b = Entry(root, text="row: %d, column: %d" % (i, j))
    #         b.grid(row=i, column=j)

    

    root.mainloop()


def update():

    s1_table = net.switches[0].cmd('ovs-ofctl dump-flows s1')
    s2_table = net.switches[1].cmd('ovs-ofctl dump-flows s2')
    # split tables by "\n" into separate entries
    s1_flows = s1_table.split('\n')
    s2_flows = s2_table.split('\n')
    # split flows by "," into separate properties
    flow_property_1 = []
    flow_property_2 = []
    for flow in s1_flows:
        flow_property_1.append(flow.replace(","," ").split(' '))
    for flow in s2_flows:
        flow_property_2.append(flow.replace(","," ").split(' '))
    # remove empty strings from list
    for i in range(0,len(flow_property_1)):
        while '' in flow_property_1[i]:
            flow_property_1[i].remove('')
    for i in range(0,len(flow_property_2)):
        while '' in flow_property_2[i]:
            flow_property_2[i].remove('')


    # reconstruct table with properties that we want
    s1_table_new = []
    s1_table_new.append('Switch 1 Flow Table\n')
    s2_table_new = []
    s2_table_new.append('Switch 2 Flow Table\n')
    print(flow_property_1)
    print(flow_property_2)
    print(" ")
    # print(" %s  | %s  | %s  | %s  | match=%s %s | %s  " % (flow_property_1[0][1], flow_property_1[0][3], flow_property_1[0][4], flow_property_1[0][5], flow_property_1[0][6], flow_property_1[0][7], flow_property_1[0][8]))
    
    # add flow entries for switch 1
    for i in range(0,6): 
        if (len(flow_property_1[i]) == 10):
            s1_table_new.append("%s | %s | %s | Match: (Protocol: %s, %s, %s) | %s | %s" %(flow_property_1[i][1], flow_property_1[i][5], flow_property_1[i][6], flow_property_1[i][7], flow_property_1[i][8], flow_property_1[9], flow_property_1[i][3], flow_property_1[i][4]))
        elif (len(flow_property_1[i]) == 8):
            s1_table_new.append("%s | %s | Match: (%s) | %s | %s | %s", % (flow_property_1[i][1], flow_property_1[i][5], flow_property_1[i][6], flow_property_1[i][7], flow_property_1[i][3], flow_property_1[i][4]))
        elif (len(flow_property_1[i]) == 7):
            s1_table_new.append("%s | %s | Match: (None) | %s | %s | %s", % (flow_property_1[i][1], flow_property_1[i][5], flow_property_1[i][6], flow_property_1[i][3], flow_property_1[i][4]))
    # add flow entries for switch 2
    for i in range(0, 7):
        if(len(flow_property_2[i]) == 9):
            s2_table_new.append("%s | %s | Match: (%s) | %s | %s | %s", % (flow_property_2[i][1], flow_property_2[i][5], flow_property_2[i][7], flow_property_2[i][8], flow_property_2[i][3], flow_property_2[i][4]))
        elif(len(flow_property_2[i]) == 10):
            s2_table_new.append("%s | %s | Match: (Protocol: %s, %s, %s) | %s | %s | %s", % (flow_property_2[i][1], flow_property_2[i][5], flow_property_2[i][6], flow_property_2[i][7], flow_property_2[i][8], flow_property_2[i][9], flow_property_2[i][3], flow_property_2[i][4]))
        elif(len(flow_property_2[i]) == 8):
            s2_table_new.append("%s | %s | Match: (%s) | %s | %s | %s", % (flow_property_2[i][1], flow_property_2[i][5], flow_property_2[i][6], flow_property_2[i][7], flow_property_2[i][3], flow_property_2[i][4]))
        elif(len(flow_property_2[i]) == 7):
            s2_table_new.append("%s | %s | Match: (None) | %s | %s | %s", % (flow_property_2[i][1], flow_property_2[i][5], flow_property_2[i][6], flow_property_2[i][3], flow_property_2[i][4]))


    s1_lbl.config(text=s1_table_new)
    s2_lbl.config(text=s2_table_new)

    root.after(1000, update)

def doneButton():
    root.destroy()
    net.stop()

if __name__ == '__main__':


    topo = ProjTopo(1)
    natSubnet = '10.0.0.0/23'
    net = Mininet(topo=topo, controller=None, autoSetMacs=True, autoStaticArp=True,ipBase=natSubnet)
    net.addController('c0', controller=RemoteController, ip="127.0.0.1", port=6633, protocols="OpenFlow13")
    net.start()

    CLI(net)
    root = tk.Tk()
    root.title("Flow tables of network switches")
    root.geometry("%dx%d+50+30" % (650,650))

    cv = tk.Canvas(width=650, height=650)
    cv.pack(side='top', fill='both', expand='yes')
    cv.create_image(0, 0, anchor='nw')

    s1_lbl = Label(root, text='0')
    s2_lbl = Label(root, text='0')

    s1_lbl.place(x=120, y=25)
    s2_lbl.place(x=120, y=300)

    done = tk.Button(cv, text="Done", command=doneButton)
    done.place(x=400, y=600)

    root.after(1000, update)

    root.mainloop()