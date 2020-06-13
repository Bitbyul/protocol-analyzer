# TCP/IP 2nd layer - Link Layer
from model.layers.DefaultLayer import *
from model.layers.networkLayers import *
from model.parseHelper import ParseHelper
from common.types import *

class DefaultLinkLayer(DefaultLayer):
    def __init__(self, *args):
        super().__init__(*args)

        self.info['layer'] = 2
        #self.upperLayer = DefaultNetworkLayer(*args)

class Ethernet(DefaultLinkLayer):

    header_size = 14 # bytes
    format_info_dict = {
        # "name": ['TYPE', start_offset, length]
        "dst_mac_addr": [DataType.MAC, 0, 6*8], 
        "src_mac_addr": [DataType.MAC, 6*8, 6*8],
        "Type": [DataType.NUM, 12*8, 2*8]
        } # bits

    info_desc_dict = { 
        "dst_mac_addr": {
            "detail": "Destination Mac Address",
            "desctype": DescType.MATCHFUNCTION,
            "func": TypeCheck.getMACType,
            "Broadcast": "Broadcast",
            "Unicast": "Unicast",
            "Multicast": "Multicast",
            "Unknown MAC": "Unknown MAC"
        },
        "src_mac_addr": {
            "detail": "Source Mac Address",
            "desctype": DescType.MATCHFUNCTION,
            "func": TypeCheck.getMACType,
            "Broadcast": "Broadcast",
            "Unicast": "Unicast",
            "Multicast": "Multicast",
            "Unknown MAC": "Unknown MAC"
        },
        "Type": {
            "desctype": DescType.MATCHWHOLE,
            "required": [],
            "default": "UNKNOWN",
            0x0800: "IP", 
            0x0806: "ARP", 
            0x0001: "ICMP",
            0x86dd: "IPv6"
            }
        }

    def __init__(self, rawdata):
        super().__init__()
        self.info['name'] = "Ethernet"
        self.info['detail'] = "The Ethernet technology"
        self.info['rawdata_length'] = int(len(rawdata)/2)

        self.header = rawdata[0:Ethernet.header_size*2]
        self.data = rawdata[Ethernet.header_size*2:]

        for i, (info_name, format_info) in enumerate(Ethernet.format_info_dict.items()):
            self.info[info_name] = ParseHelper.getData(self.header, format_info)

        Type = self.getDesc("Type", self.info["Type"])

        # TODO: CREATE FACTORY CLASS
        if(Type == "IP"):
            self.upperLayer = IP(self.data)
        elif(Type == "ARP"):
            self.upperLayer = ARP(self.data)
        elif(Type == "ICMP"):
            self.upperLayer = ICMP(self.data)
        elif(Type == "IPv6"):
            self.upperLayer = IPv6(self.data)
        else:
            self.upperLayer = DefaultNetworkLayer(self.data)

