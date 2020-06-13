from model.parseHelper import ParseHelper

class DataParser():
    def __init__(self):
        pass

    # Unused From 2020/06/11 Replaced with detailParse
    @staticmethod
    def simpleParse(rawdata):
        protocols = []
        length = int(len(rawdata)/2)
        try:
            dst_mac = ParseHelper.getMACFormat(rawdata, 0, 12*8)
            src_mac = ParseHelper.getMACFormat(rawdata, 12*8, 24*8)

            ethernet_type = ParseHelper.getNumber(rawdata, 24*8, 28*8)
            if(ethernet_type==0x0800):
                protocols.append("IP")
            else:
                protocols.append("UNKNOWN")
            
            return dict(src_mac=src_mac, dst_mac=dst_mac, src_ip='127.0.0.1', dst_ip='127.0.0.2', protocols=protocols, length=length, info='ㅎㅇㅎㅇ', rawdata=rawdata)
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def simpleParseFromProtocol(protocol):
        pass

    @staticmethod
    def getProtocolNameListFromProtocol(protocol):
        return DataParser.getProtocolNameListFromProtocolInfo(protocol.getData())

    @staticmethod
    def getProtocolNameListFromProtocolInfo(protocol_info):
        protocol_list = []
        # except layer 2

        while True:
            if not ("upperLayer" in protocol_info): break
            protocol_info = protocol_info['upperLayer']
            
            if ('name' not in protocol_info or protocol_info['name'] == "UNKNOWN"): break
            protocol_list.append(protocol_info['name'])
        return protocol_list


    @staticmethod
    def getIPProtocolNameByNum(protocol_number):
        protocol_name = "UNKNOWN"
        f = open("PROTOCOLS_IP.txt", 'r')
        while True:
            line = f.readline()
            if not line: break
            if line.strip()=="" or line.strip()[0] == "#": continue
            linedata = line.split("\t")
            if(protocol_number == int(linedata[1])):
                protocol_name = linedata[2]
                break
        f.close()

        if protocol_name.strip() == "": protocol_name = "UNKNOWN"
        return protocol_name

    @staticmethod
    def getServiceName(port_number, protocol_name):
        service_name = ["UNKNOWN",None]
        match = str(port_number)+"/"+protocol_name.lower()
        f = open("SERVICES.txt", 'r')
        while True:
            line = f.readline()
            if not line: break
            if line.strip()=="" or line.strip()[0] == "#" : continue
            linedata = line.split()
            if(match == linedata[1]):
                service_name[0] = linedata[0]
                if(line.find("#") > -1):
                    service_name[1] = line[line.find("#")+1:].strip()
                break
        f.close()

        return service_name