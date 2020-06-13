# TCP/IP 4th layer - Transport Layer
from model.layers.DefaultLayer import *
from model.layers.applicationLayers import *
from model.parseHelper import ParseHelper
from common.types import *

class DefaultTrnansportLayer(DefaultLayer):
    def __init__(self, *args):
        super().__init__(*args)

        self.info['layer'] = 4
        #self.upperLayer = DefaultApplicationLayer(*args)

class TCP(DefaultTrnansportLayer):

    header_size = 20 # bytes. could be increased.
    format_info_dict = {
        "src_port": [DataType.NUM, 0, 16], 
        "dst_port": [DataType.NUM, 16, 16],
        "seq_num": [DataType.NUM, 32, 32],
        "ack_num": [DataType.NUM, 64, 32],
        "header_length": [DataType.NUM, 96, 4],
        #"reserved": [DataType.NUM, 100, 6],
        "control_bits": [DataType.NUM, 100, 12],
        "window_size": [DataType.NUM, 112, 16],
        "checksum": [DataType.HEX, 128, 16],
        "urgent_pointer": [DataType.NUM, 144, 16]
        } # bits

    info_desc_dict = { 
        "src_port": {
            "detail": "Source port",
            "desctype": DescType.MATCHFROMSERVICE,
            "required": [],
            "headtext": "Port:"
        },
        "dst_port": {
            "detail": "Destination port",
            "desctype": DescType.MATCHFROMSERVICE,
            "required": [],
            "headtext": "Port:"
        },
        "seq_num": {
            "detail": "Sequence number",
            "desctype": DescType.NUMBER,
            "required": [],
        },
        "ack_num": {
            "detail": "Acknowledgement number",
            "desctype": DescType.NUMBER,
            "required": [],
        },
        "header_length": {
            "detail": "Header length",
            "desctype": DescType.BYTESMUL4,
            "required": [],
        },
        "control_bits": {
            "detail": "Control bits",
            "desctype": DescType.FUNCTIONRESULT,
            "func": TypeCheck.getTCPControlBitsDetail,
            "required": [],
        },
        "window_size": {
            "detail": "Window size",
            "desctype": DescType.BYTES,
            "required": [],
        },
        "checksum": {
            "detail": "Checksum",
        },
        "urgent_pointer": {
            "detail": "Urgent pointer",
            "desctype": DescType.MATCHWHOLE,
            "required": [],
            "default": "Urgent",
            0x0000: "Not Urgent"
        },
        "option": {
            "detail": "Option"
        }
    }

    def __init__(self, rawdata):
        super().__init__()
        self.info['name'] = "TCP"
        self.info['detail'] = "The Transmission Control Protocol"
        self.info['rawdata_length'] = int(len(rawdata)/2)

        # update additional protocol information
        for i, (info_name, format_info) in enumerate(self.format_info_dict.items()):
            self.info[info_name] = ParseHelper.getData(rawdata, format_info)

        # correct header length
        self.header_size = self.info['header_length'] * 4

        # rest for option (HARD CODING TEMPORARY!!) TODO: Need some DescType??
        if not self.header_size == 20:
            self.info['option'] = "0x"+rawdata[160//4:160//4+self.header_size]

        # split header and data
        self.header = rawdata[0:self.header_size*2]
        self.data = rawdata[self.header_size*2:]

        self.upperLayer = DefaultApplicationLayer(self.data)
            
class UDP(DefaultTrnansportLayer):

    header_size = 8 # bytes.
    format_info_dict = {
        "src_port": [DataType.NUM, 0, 16], 
        "dst_port": [DataType.NUM, 16, 16],
        "total_length": [DataType.NUM, 32, 16],
        "checksum": [DataType.NUM, 48, 16],
        } # bits

    info_desc_dict = { 
        "src_port": {
            "detail": "Source Port",
            "desctype": DescType.MATCHFROMSERVICE,
            "headtext": "Port:"
        },
        "dst_port": {
            "detail": "Destination Port",
            "desctype": DescType.MATCHFROMSERVICE,
            "headtext": "Port:"
        },
        "total_length": {
            "detail": "Total Length",
            "desctype": DescType.BYTES,
        },
        "checksum": {
            "detail": "Checksum",
        }
    }

    def __init__(self, rawdata):
        super().__init__()
        self.info['name'] = "UDP"
        self.info['detail'] = "The User Datagram Protocol"
        self.info['rawdata_length'] = int(len(rawdata)/2)

        # update additional protocol information
        for i, (info_name, format_info) in enumerate(self.format_info_dict.items()):
            self.info[info_name] = ParseHelper.getData(rawdata, format_info)

        # split header and data
        self.header = rawdata[0:self.header_size*2]
        self.data = rawdata[self.header_size*2:]

        self.upperLayer = DefaultApplicationLayer(self.data, )

class SCTP(DefaultTrnansportLayer):

    header_size = 12 # bytes.
    format_info_dict = {
        "src_port": [DataType.NUM, 0, 16], 
        "dst_port": [DataType.NUM, 16, 16],
        "verification_tag": [DataType.NUM, 32, 32],
        "checksum": [DataType.NUM, 64, 32],
        } # bits

    info_desc_dict = { 
        "src_port": {
            "detail": "Source Port",
            "desctype": DescType.MATCHFROMSERVICE,
            "headtext": "Port:"
        },
        "dst_port": {
            "detail": "Destination Port",
            "desctype": DescType.MATCHFROMSERVICE,
            "headtext": "Port:"
        },
        "verification_tag": {
            "detail": "Verification Tag",
            "desctype": DescType.NUMBER,
        },
        "checksum": {
            "detail": "Checksum",
        }
    }

    def __init__(self, rawdata):
        super().__init__()
        self.info['name'] = "SCTP"
        self.info['detail'] = "The Stream Control Transmission Protocol"
        self.info['rawdata_length'] = int(len(rawdata)/2)

        # update additional protocol information
        for i, (info_name, format_info) in enumerate(self.format_info_dict.items()):
            self.info[info_name] = ParseHelper.getData(rawdata, format_info)

        # split header and data
        self.header = rawdata[0:self.header_size*2]
        self.data = rawdata[self.header_size*2:]

        self.upperLayer = DefaultApplicationLayer(self.data)