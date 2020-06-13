# TCP/IP 3rd layer - Network Layer
from model.layers.DefaultLayer import *
from model.layers.transportLayers import *
from model.parseHelper import ParseHelper
from common.types import *

class DefaultNetworkLayer(DefaultLayer):
    def __init__(self, *args):
        super().__init__(*args)

        self.info['layer'] = 3
        #self.upperLayer = DefaultTrnansportLayer(*args)

class ARP(DefaultNetworkLayer):
        
    header_size = 0 # bytes. must be increased.
    format_info_dict = {
        "hardware_type": [DataType.NUM, 0, 16], 
        "protocol_type": [DataType.NUM, 16, 16],
        "hardware_length": [DataType.NUM, 32, 8],
        "protocol_length": [DataType.NUM, 40, 8],
        "operation": [DataType.NUM, 48, 16],
        } # bits
        
    info_desc_dict = { 
        "hardware_type": {
            "detail": "H/W Type",
            "desctype": DescType.MATCHWHOLE,
            "required": [],
            "default": "UNKNOWN",
            0x00001: "Ethernet"
        },
        "protocol_type": {
            "detail": "Protocol Type",
            "desctype": DescType.MATCHWHOLE,
            "required": [],
            "default": "UNKNOWN",
            0x0800: "IP"
        },
        "hardware_length": {
            "detail": "H/W Address Size",
            "desctype": DescType.BYTES,
            "required": []
        },
        "protocol_length": {
            "detail": "Protocol Address Size",
            "desctype": DescType.BYTES,
            "required": []
        },
        "operation": {
            "detail": "Operation",
            "desctype": DescType.MATCHWHOLE,
            "required": [],
            0x0001: "ARP Request",
            0x0002: "ARP Reply"
        },
        "src_hw_addr": {
            "detail": "Source H/W Address",
            "desctype": DescType.MATCHFUNCTION,
            "func": TypeCheck.getMACType,
            "Broadcast": "Broadcast",
            "Unicast": "Unicast",
            "Multicast": "Multicast",
            "Unknown MAC": "Unknown MAC"
        },
        "src_proto_addr": {
            "detail": "Source Protocol Address"
        },
        "dst_hw_addr": {
            "detail": "Destination H/W Address",
            "desctype": DescType.MATCHFUNCTION,
            "func": TypeCheck.getMACType,
            "Broadcast": "Broadcast",
            "Unicast": "Unicast",
            "Multicast": "Multicast",
            "Unknown MAC": "Unknown MAC"
        },
        "dst_proto_addr": {
            "detail": "Source Protocol Address"
        } 
    }

    def __init__(self, rawdata):
        super().__init__()
        self.info['name'] = "ARP"
        self.info['detail'] = "The Address Resolution Protocol"
        self.info['rawdata_length'] = int(len(rawdata)/2)

        # update additional protocol information
        for i, (info_name, format_info) in enumerate(ARP.format_info_dict.items()):
            self.info[info_name] = ParseHelper.getData(rawdata, format_info)

        # update HW and protocol address information
        address_format_info_dict = {
            "src_hw_addr": [DataType.MAC, 64, self.info['hardware_length']*8],
            "src_proto_addr": [DataType.IP, 64+self.info['hardware_length']*8, 
                                self.info['protocol_length']*8],
            "dst_hw_addr": [DataType.MAC, 64+self.info['hardware_length']*8+self.info['protocol_length']*8, 
                                self.info['hardware_length']*8],
            "dst_proto_addr": [DataType.IP, 64+self.info['hardware_length']*16+self.info['protocol_length']*8,
                                self.info['protocol_length']*8]
        }
        for i, (info_name, format_info) in enumerate(address_format_info_dict.items()):
            self.info[info_name] = ParseHelper.getData(rawdata, format_info)

        # correct header length
        self.header_size = 64 + self.info['hardware_length']*2 + self.info['protocol_length']*2
        
        # split header and data
        self.header = rawdata[0:self.header_size*2]
        self.data = rawdata[self.header_size*2:]
            
        # set upperLayer Protocol
        # ARP END
        self.upperLayer = DefaultTrnansportLayer(self.data)

class IP(DefaultNetworkLayer):

    header_size = 20 # bytes. could be increased up to 60.
    format_info_dict = {
        "version": [DataType.NUM, 0, 4], 
        "header_length": [DataType.NUM, 4, 4],
        "service_type": [DataType.NUM, 8, 8],
        "total_length": [DataType.NUM, 16, 16],
        "identification": [DataType.NUM, 32, 16],
        "flags": [DataType.NUM, 48, 4],
        "fragmentation_offset": [DataType.NUM, 51, 13],
        "ttl": [DataType.NUM, 64, 8],
        "protocol": [DataType.NUM, 72, 8],
        "header_checksum": [DataType.HEX, 80, 16],
        "src_ip_addr": [DataType.IP, 96, 32],
        "dst_ip_addr": [DataType.IP, 128, 32]
        } # bits
        
    info_desc_dict = { 
        "version": {
            "detail": "Version",
            "desctype": DescType.MATCHWHOLE,
            "required": [],
            0x04: "Internet Protocol version 4", 
            0x06: "Internet Protocol version 6"
        },
        "header_length": {
            "detail": "Header Length",
            "desctype": DescType.BYTESMUL4,
            "required": [],
            "tailtext": "header"
        },
        "service_type": {
            "detail": "Service Type",
            "desctype": DescType.MATCHWHOLE,
            "required": [],
            "default": "Unknown service type",
            0x00: "No service type"
        },
        "total_length": {
            "detail": "Total Length",
            "desctype": DescType.BYTES,
            "required": [],
            "tailtext": "payload"
        },
        "identification": {
            "detail": "Identification",
        },
        "flags": {
            "detail": "Flags",
            "desctype": DescType.FUNCTIONRESULT,
            "func": TypeCheck.getIPFlagsDetail
        },
        "fragmentation_offset": {
            "detail": "Fragmentation Offset",
            "desctype": DescType.MATCHWHOLE,
            "required": [],
            "default": "Following Fragment(Not the first Fragment!)",
            0x0: "First Fragment"
        },
        "ttl": {
            "detail": "TTL(Time-To-Live)",
            "desctype": DescType.NUMBER,
            "required": [],
            "tailtext": "hops"
        },
        "protocol": {
            "detail": "Protocol",
            "desctype": DescType.MATCHFROMIPPROTOCOL,
            "required": []
        },
        "header_checksum": {
            "detail": "Checksum",
        },
        "src_ip_addr": {
            "detail": "Source IP Address",
        },
        "dst_ip_addr": {
            "detail": "Destination IP Address",
        }
    }

    def __init__(self, rawdata):
        super().__init__()
        self.info['name'] = "IP"
        self.info['detail'] = "The Internet Protocol"
        self.info['rawdata_length'] = int(len(rawdata)/2)
        
        # update additional protocol information
        for i, (info_name, format_info) in enumerate(IP.format_info_dict.items()):
            self.info[info_name] = ParseHelper.getData(rawdata, format_info)

        # correct header length
        self.header_size = self.info['header_length'] * 4
        
        # split header and data
        self.header = rawdata[0:IP.header_size*2]
        self.data = rawdata[IP.header_size*2:]

        # update detail-needed data info dict (_val)
        # update protocol data
        #self.info['protocol'] = "UNKNOWN"
        protocol = self.getDesc("protocol", self.info["protocol"])
        #self.correctAllDetailNeededKey()
        
        # set upperLayer Protocol
        # TODO: CREATE FACTORY CLASS
        if(protocol == "TCP"):
            self.upperLayer = TCP(self.data)
        elif(protocol == "UDP"):
            self.upperLayer = UDP(self.data)
        elif(protocol == "ICMP"):
            self.upperLayer = ICMP(self.data)
        elif(protocol == "SCTP"):
            self.upperLayer = SCTP(self.data)
        else:
            self.upperLayer = DefaultTrnansportLayer(self.data, protocol)
            
class ICMP(DefaultNetworkLayer):

    header_size = 20 # bytes. could be increased.
    format_info_dict = {
        'Type': [DataType.NUM, 8, 8],
        'code': [DataType.NUM, 8, 8],
        'checksum': [DataType.HEX, 16, 16]
        } # bits

    info_desc_dict = { 
        "Type": {
            "desctype": DescType.MATCHWHOLE,
            "required": [],
            3: "Error-reporting: Destination unreachable", 
            4: "Error-reporting: Source quench", 
            5: "Error-reporting: Redirection",
            11: "Error-reporting: Time exceeded",
            12: "Error-reporting: Parameter problem",
            8: "Query: Echo request",
            0: "Query: Echo reply",
            13: "Query: Timestamp request",
            14: "Query: Timestamp reply"
        },
        "code": {
            "detail": "Code",
            "desctype": DescType.MATCHWHOLE,
            "required": ["Type"]

        },
        "checksum": {
            "detail": "Checksum"
        },
        "identifier": {
            "detail": "Identifier",
            "desctype": DescType.NUMBER
        },
        "sequence_number": {
            "detail": "Sequence Number",
            "desctype": DescType.NUMBER
        }
    }

    def __init__(self, rawdata):
        super().__init__()
        self.info['name'] = "ICMP"
        self.info['detail'] = "The Internet Control Message Protocol"
        self.info['rawdata_length'] = int(len(rawdata)/2)
        
        # update additional protocol information
        for i, (info_name, format_info) in enumerate(self.format_info_dict.items()):
            self.info[info_name] = ParseHelper.getData(rawdata, format_info)

        # update additional protocol information based on Type(Error-reporting(3,4,5,11,12) or Query(8,0,13,14))
        if(self.info['Type'] in [8,0,13,14]):
            # Query Message
            format_info_dict_addition = {
                'identifier': [DataType.NUM, 32, 16],
                'sequence_number': [DataType.NUM, 48, 16]
            }
            for i, (info_name, format_info) in enumerate(format_info_dict_addition.items()):
                self.info[info_name] = ParseHelper.getData(rawdata, format_info)

            self.format_info_dict.update(format_info_dict_addition)


        """
        # update Message Type (Error-reporting or Query message)
        if self.info['code'] in [0x00, 0x08, 0x13, 0x14]: self.info['msgType'] = "Query"
        elif self.info['code'] in [0x03, 0x04, 0x05, 0x11, 0x12]: self.info['msgType'] = "Error-reporting"
        else: self.info['msgType'] = "UNKNOWN"
        """
        
        
class IPv6(DefaultNetworkLayer):

    header_size = 40 # bytes. Fixed.
    format_info_dict = {
        "version": [DataType.NUM, 0, 4],
        "traffic_class": [DataType.NUM, 4, 8],
        "flow_label": [DataType.NUM, 12, 20],
        "payload_length": [DataType.NUM, 32, 16],
        "next_header": [DataType.NUM, 48, 8], # Transport Layer Protocol
        "hop_limit": [DataType.NUM, 56, 8],
        "src_ip_addr": [DataType.IPv6, 64, 128],
        "dst_ip_addr": [DataType.IPv6, 192, 128]
        } # bits
        
    info_desc_dict = { 
        "version": {
            "detail": "Version",
            "desctype": DescType.MATCHWHOLE,
            "required": [],
            0x06: "Internet Protocol version 6"
        },
        "traffic_class": {
            "detail": "Traffic Class",
        },
        "flow_label": {
            "detail": "Flow Label",
        },
        "payload_length": {
            "detail": "Payload Length",
            "desctype": DescType.BYTES,
            "required": [],
            "tailtext": "payload"
        },
        "next_header": {
            "detail": "Protocol",
            "desctype": DescType.MATCHFROMIPPROTOCOL,
            "required": []
        },
        "hop_limit": {
            "detail": "TTL(Time-To-Live)",
            "desctype": DescType.NUMBER,
            "required": [],
            "tailtext": "hops"
        },
        "src_ip_addr": {
            "detail": "Source IP Address",
        },
        "dst_ip_addr": {
            "detail": "Destination IP Address",
        }
    }

    def __init__(self, rawdata):
        super().__init__()
        self.info['name'] = "IPv6"
        self.info['detail'] = "The Internet Protocol Version 6"
        self.info['rawdata_length'] = int(len(rawdata)/2)
        
        # update additional protocol information
        for i, (info_name, format_info) in enumerate(self.format_info_dict.items()):
            self.info[info_name] = ParseHelper.getData(rawdata, format_info)
        
        # split header and data
        self.header = rawdata[0:self.header_size*2]
        self.data = rawdata[self.header_size*2:]

        # update detail-needed data info dict (_val)
        # update protocol data
        #self.info['protocol'] = "UNKNOWN"
        next_header = self.getDesc("next_header", self.info["next_header"])
        #self.correctAllDetailNeededKey()
        
        # set upperLayer Protocol
        # TODO: CREATE FACTORY CLASS
        if(next_header == "TCP"):
            self.upperLayer = TCP(self.data)
        elif(next_header == "UDP"):
            self.upperLayer = UDP(self.data)
        elif(next_header == "ICMP"):
            self.upperLayer = ICMP(self.data)
        elif(next_header == "SCTP"):
            self.upperLayer = SCTP(self.data)
        else:
            self.upperLayer = DefaultTrnansportLayer(self.data)