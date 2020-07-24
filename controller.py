from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ether_types, ipv4

class AppRouting(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(AppRouting, self).__init__(*args, **kwargs)

    #event handler for new switches
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)            
    def switch_features_handler(self, ev):
        # get switch                                      
        datapath = ev.msg.datapath                                              
        # get parsing library for protocol used by switch (OpenFlow 1.x)
        parser = datapath.ofproto_parser
        # get dpid
        dpid = str(hex(datapath.id))[2:].zfill(16)                            
        self.logger.info("DPID is %s", dpid)

        # nat switch case
        if (int(dpid[14:16]) == 1):
            self.logger.info("nat switch")
            self.nat_switch(ev)
        # consumer switch case    
        elif (int(dpid[14:16]) == 2):
            self.logger.info("Consumer switch")
            self.consumer_switch(ev)
        else:
            self.logger.info("Hit else statment, DPID is %s", dpid)

    def consumer_switch(self, ev):
        # get switch                                      
        datapath = ev.msg.datapath                                              
        # get parsing library for protocol used by switch (OpenFlow 1.x)
        parser = datapath.ofproto_parser
        # get dpid
        dpid = str(hex(datapath.id))[2:].zfill(16)                            
        self.logger.info("DPID is %s", dpid)

        # create flow entries (outgoing to internet)
        matches = []
        matches.append(parser.OFPMatch(in_port=1, eth_type=0x800, udp_dst=443, ip_proto = 0x11))
        matches.append(parser.OFPMatch(in_port=1, eth_type=0x800, udp_dst=80, ip_proto = 0x11))
        matches.append(parser.OFPMatch(in_port=1, eth_type=0x800, tcp_dst=443, ip_proto = 0x06))
        matches.append(parser.OFPMatch(in_port=1, eth_type=0x800, tcp_dst=80, ip_proto = 0x06))

        # create action entry (outgoing)
        action = parser.OFPActionOutput(3,0)
        # add flow entries (outgoing)
        for match in matches:
            self.add_flow(datapath, 10, match, action)   

        # create default outgoing match
        match = parser.OFPMatch(in_port=1)
        # create default outgoing action
        action = parser.OFPActionOutput(2,0)
        # add default outgoing flow entry
        self.add_flow(datapath, 2, match, action)

        # create default incoming match
        match = parser.OFPMatch()
        # create default incoming action
        action = parser.OFPActionOutput(1,0)
        # add default incoming flow entry
        self.add_flow(datapath, 1, match, action)

    def nat_switch(self, ev):
        # get switch                                      
        datapath = ev.msg.datapath                                              
        # get parsing library for protocol used by switch (OpenFlow 1.x)
        parser = datapath.ofproto_parser
        # get dpid
        dpid = str(hex(datapath.id))[2:].zfill(16)                            
        self.logger.info("DPID is %s", dpid)

        # create flow entries (incoming to nat switch)
        matches = []
        matches.append(parser.OFPMatch(in_port=1, eth_type=0x800, udp_dst=443, ip_proto = 0x11))
        matches.append(parser.OFPMatch(in_port=1, eth_type=0x800, udp_dst=80, ip_proto = 0x11))
        matches.append(parser.OFPMatch(in_port=1, eth_type=0x800, tcp_dst=443, ip_proto = 0x06))
        matches.append(parser.OFPMatch(in_port=1, eth_type=0x800, tcp_dst=80, ip_proto = 0x06))


        # create action entry (incoming)
        actions = parser.OFPActionOutput(3,0)
        # add flow entries (incoming)
        for match in matches:
            self.add_flow(datapath, 10, match, actions)

        # create default incoming match
        match = parser.OFPMatch(in_port=1)
        # create default incoming action
        action = parser.OFPActionOutput(2,0)
        # add default incoming flow entry
        self.add_flow(datapath, 1, match, action)

        # create default outgoing match
        match = parser.OFPMatch()
        # create default outgoing action
        action = parser.OFPActionOutput(1,0)
        # add default outgoing flow entry
        self.add_flow(datapath, 1, match, action)
        
    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # create instruction using apply action
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                            [actions])]

        # create flow mod from instruction and other arguments
        mod = parser.OFPFlowMod(datapath=datapath,command=ofproto.OFPFC_ADD,priority=priority,match=match,instructions=inst)

        # send flow mod to switch
        datapath.send_msg(mod)