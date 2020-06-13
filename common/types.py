class DataType:
    HEX = "HEX" # hex number
    NUM = "NUM" # normal decimal number
    MAC = "MAC" # MAC address format
    IP = "IP" # IP address format
    IPv6 = "IPv6" # IPv6 address format

class DescType:
    MATCHWHOLE = "MATCHWHOLE" # Whole Data Match
    MATCHCONTAIN = "MATCHCONTAIN" # Part Data Match
    MATCHSTARTFROM = "MATCHSTARTFROM" # Data Start Special Pattern Match
    MATCHFUNCTION = "MATCHFUNCTION" # Find Match Data By A Function
    MATCHFROMIPPROTOCOL = "MATCHFROMIPPROTOCOL" # Match From IP Protocol List File (PROTOCOLS_IP.txt)
    MATCHFROMSERVICE = "MATCHFROMSERVICE" # Match From Service List File (SERVICES.txt)
    NUMBER = "NUMBER" # For decimal number
    BYTES = "BYTES" # For decimal bytes
    BYTESMUL4 = "BYTESMUL4" # *4 bytes
    FUNCTIONRESULT = "FUNCTIONRESULT" # Function Result

class TypeCheck:
    @staticmethod
    def getMACType(macaddr):
        try:
            macaddr = macaddr.upper()
            bit = int(macaddr[0:2],16) % 2
            if(macaddr=="FF:FF:FF:FF:FF:FF"): return "Broadcast"
            if(macaddr=="00:00:00:00:00:00"): return "Unknown MAC"
            elif(bit==1): return "Multicast"

            return "Unicast"
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def getIPFlagsDetail(flags):
        bits_dict = [
            ["Reserve", ["Unset", "Set"]],
            ["Don't Fragment", ["Able to fragment", "Unble to fragment"]],
            ["More", ["No more fragments", "More fragments"]],
        ]
        flags = str(bin(flags))[2:].rjust(4,"0")[:3]
        detail_dict = {'DESC': flags}
        for i, b in enumerate(flags):
            if(i >= len(bits_dict)): break
            detail_dict[bits_dict[i][0]] = b, bits_dict[i][1][int(b)]
        return detail_dict

    @staticmethod
    def getTCPControlBitsDetail(control_bits):
        bits_dict = [
            ["Urgent", ["Not urgent", "Urgent"]],
            ["Ack", ["Not Acknowlegment", "Acknowlegment"]],
            ["Push", ["Normal", "Push"]],
            ["Reset", ["Normal", "Reset"]],
            ["Syn", ["Not Connection Setup", "Connection Setup"]],
            ["Fin", ["Not Connection Release", "Connection Release"]]
        ]
        control_bits = str(bin(control_bits))[2:].rjust(6,"0")
        detail_dict = {'DESC': control_bits}
        for i, b in enumerate(control_bits):
            if(i >= len(bits_dict)): break
            detail_dict[bits_dict[i][0]] = b, bits_dict[i][1][int(b)]
        return detail_dict