from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ether_types, ipv4

# GUI Tkinter packages
import Tkinter as tk
from Tkinter import *
import tkMessageBox

HIGH_BW_LINK = 3
GENERIC_BW_LINK = 2
HOST_LINK = 1
INTERNET_LINK = 1


class AppRouting(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(AppRouting, self).__init__(*args, **kwargs)

        # GUI
        self.options = []

        self.root = tk.Tk()
        self.root.title("Application-based routing")

        bgimage = tk.PhotoImage(file = "images/background_1.png")
        w = bgimage.width()
        h = bgimage.height()
        self.root.geometry("%dx%d+50+30" % (650,h))
        # Create canvas for background image
        cv = tk.Canvas(width=w, height=h)
        cv.pack(side='top', fill='both', expand='yes')
        # cv.create_image(0, 0, image=bgimage, anchor='nw')
        cv.create_image(0, 0, anchor='nw')

        # Create buttons
        netflix_img = tk.PhotoImage(file="images/netflix_50.png")
        netflix = tk.Checkbutton(cv, image=netflix_img, command=self.netflixButton)
        netflix.place(anchor='nw', x=120, y=250)

        youtube_img = tk.PhotoImage(file="images/youtube_50.png")
        youtube = tk.Checkbutton(cv, image=youtube_img, command=self.youtubeButton)
        youtube.place(anchor='nw', x=240, y=250)

        twitch_img = tk.PhotoImage(file="images/twitch_50.png")
        twitch = tk.Checkbutton(cv, image=twitch_img, command=self.twitchButton)
        twitch.place(anchor='nw', x=360, y=250)

        primevideo_img = tk.PhotoImage(file="images/primevideo_50.png")
        primevideo = tk.Checkbutton(cv, image=primevideo_img, command=self.primeVideoButton)
        primevideo.place(anchor='nw', x=120, y=350)

        appletv_img = tk.PhotoImage(file="images/appletv_50.png")
        appletv = tk.Checkbutton(cv, image=appletv_img, command=self.appleTVButton)
        appletv.place(anchor='nw', x=240, y=350)

        disneyplus_img = tk.PhotoImage(file="images/disneyplus_50.png")
        disneyplus = tk.Checkbutton(cv, image=disneyplus_img, command=self.disneyPlusButton)
        disneyplus.place(anchor='nw', x=360, y=350)

        stan_img = tk.PhotoImage(file="images/stan_50.png")
        stan = tk.Checkbutton(cv, image=stan_img, command=self.stanButton)
        stan.place(anchor='nw', x=120, y=450)

        binge_img = tk.PhotoImage(file="images/binge_50.png")
        binge = tk.Checkbutton(cv, image=binge_img, command=self.bingeButton)
        binge.place(anchor='nw', x=240, y=450)

        plex_img = tk.PhotoImage(file="images/plex_50.png")
        plex = tk.Checkbutton(cv, image=plex_img, command=self.plexButton)
        plex.place(anchor='nw', x=360, y=450)

        # add a done button
        done = tk.Button(cv, text="Done", command=self.doneButton)
        done.place(anchor='nw', x=400, y=600)

        self.root.mainloop()

    def netflixButton(self):
        if('NETFLIX' not in self.options):
            self.options.append('NETFLIX')
            print('added Netflix')
        else:
            self.options.remove('NETFLIX')
            print('removed Netflix')

    def youtubeButton(self):
        if('YOUTUBE' not in self.options):
            self.options.append('YOUTUBE')
            print('added Youtube')
        else:
            self.options.remove('YOUTUBE')
            print('removed Youtube')

    def twitchButton(self):
        if('TWITCH' not in self.options):
            self.options.append('TWITCH')
            print('added Twitch')
        else:
            self.options.remove('TWITCH')
            print('removed Twitch')

    def primeVideoButton(self):
        if('PRIME' not in self.options):
            self.options.append('PRIME')
            print('added Prime')
        else:
            self.options.remove('PRIME')
            print('removed Prime')

    def appleTVButton(self):
        if('APPLE' not in self.options):
            self.options.append('APPLE')
            print('added Apple TV')
        else:
            self.options.remove('APPLE')
            print('removed Apple TV')

    def disneyPlusButton(self):
        if('DISNEY' not in self.options):
            self.options.append('DISNEY')
            print('added Disney')
        else:
            self.options.remove('DISNEY')
            print('removed Disney')

    def stanButton(self):
        if('STAN' not in self.options):
            self.options.append('STAN')
            print('added Stan')
        else:
            self.options.remove('STAN')
            print('removed Stan')

    def bingeButton(self):
        if('BINGE' not in self.options):
            self.options.append('BINGE')
            print('added BINGE')
        else:
            self.options.remove('BINGE')
            print('removed Binge')

    def plexButton(self):
        if('PLEX' not in self.options):
            self.options.append('PLEX')
            print('added Plex')
        else:
            self.options.remove('PLEX')
            print('removed Plex')

    def doneButton(self):
        self.root.destroy()



    #event handler for new switches
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)            
    def switch_features_handler(self, ev):
        # get switch                                      
        datapath = ev.msg.datapath                                              
        # get parsing library for protocol used by switch (OpenFlow 1.x)
        parser = datapath.ofproto_parser
        # get dpid
        dpid = str(hex(datapath.id))[2:].zfill(16)                            
        # self.logger.info("DPID is %s", dpid)

        # nat switch case
        if (int(dpid[14:16]) == 1):
            self.nat_switch(ev)
            self.logger.info("NAT switch is ready")
        # consumer switch case    
        elif (int(dpid[14:16]) == 2):
            self.consumer_switch(ev)
            self.logger.info("Consumer switch is ready")
        else:
            self.logger.info("DPID unrecognised: %s", dpid)

    def consumer_switch(self, ev):
        # get switch                                      
        datapath = ev.msg.datapath                                              
        # get parsing library for protocol used by switch (OpenFlow 1.x)
        parser = datapath.ofproto_parser
        # get dpid
        dpid = str(hex(datapath.id))[2:].zfill(16)                            
        # self.logger.info("DPID is %s", dpid)

        prefix = "45.57.70.0"
        mask = "255.255.254.0"
        # create flow entries (outgoing to internet)
        matches = []
        if('NETFLIX' in self.options):
            # netflix priority match
            print("prioritising netflix")
            matches.append(parser.OFPMatch(in_port=HOST_LINK, eth_type=0x800, tcp_dst=443, ip_proto=0x06, ipv4_dst=(prefix,mask)))
        if('YOUTUBE' in self.options):
            # youtube priority match
            ##
            print("prioritising youtube")

        # create action entry (outgoing)
        action = parser.OFPActionOutput(HIGH_BW_LINK,0)
        # add flow entries (outgoing)
        for match in matches:
            self.add_flow(datapath, 10, match, action)   

        # create default outgoing match
        match = parser.OFPMatch(in_port=HOST_LINK)
        # create default outgoing action
        action = parser.OFPActionOutput(GENERIC_BW_LINK,0)
        # add default outgoing flow entry
        self.add_flow(datapath, 2, match, action)

        # create default incoming match to host's IP address
        match = parser.OFPMatch(eth_type=0x800, ipv4_dst='10.0.1.1')
        # create incoming action with priority 10
        action = parser.OFPActionOutput(HOST_LINK,0)
        # add default incoming flow entry
        self.add_flow(datapath, 11, match, action)


        # create default incoming match
        match = parser.OFPMatch()
        # create default incoming action
        action = parser.OFPActionOutput(HOST_LINK,0)
        # add default incoming flow entry
        self.add_flow(datapath, 1, match, action)

    def nat_switch(self, ev):
        # get switch                                      
        datapath = ev.msg.datapath                                              
        # get parsing library for protocol used by switch (OpenFlow 1.x)
        parser = datapath.ofproto_parser
        # get dpid
        dpid = str(hex(datapath.id))[2:].zfill(16)                            
        # self.logger.info("DPID is %s", dpid)

        # netflix subnet 
        prefix = "45.57.70.0"
        mask = "255.255.254.0"

        # create flow entries (incoming to nat switch)
        matches = []

        if('NETFLIX' in self.options):
            # prioritising netflix
            print("prioritising netflix")
            matches.append(parser.OFPMatch(in_port=INTERNET_LINK, eth_type=0x800, tcp_src=443, ip_proto=0x06, ipv4_src=(prefix,mask)))
        
        if('YOUTUBE' in self.options):
            # prioritising youtube
            print("prioritising youtube")
            # youtube entry
            ##

        # create action entry (incoming)
        actions = parser.OFPActionOutput(HIGH_BW_LINK,0)
        # add flow entries (incoming)
        for match in matches:
            self.add_flow(datapath, 10, match, actions)

        # create default incoming match
        match = parser.OFPMatch(in_port=INTERNET_LINK)
        # create default incoming action
        action = parser.OFPActionOutput(GENERIC_BW_LINK,0)
        # add default incoming flow entry
        self.add_flow(datapath, 3, match, action)

        # create default outgoing match
        match = parser.OFPMatch()
        # create default outgoing action
        action = parser.OFPActionOutput(INTERNET_LINK,0)
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