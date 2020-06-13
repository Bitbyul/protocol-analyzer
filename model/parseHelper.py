# Parse Data from hex data helper class.
from common.types import *

class ParseHelper:
    @staticmethod
    def getData(rawdata, format_info):
        data_type = format_info[0]
        if(data_type==DataType.NUM):
            return ParseHelper.getNumber(rawdata, format_info[1], format_info[2])
        elif(data_type==DataType.HEX):
            return ParseHelper.getHEX(rawdata, format_info[1], format_info[2])
        elif(data_type==DataType.MAC):
            return ParseHelper.getMACFormat(rawdata, format_info[1], format_info[2])
        elif(data_type==DataType.IP):
            return ParseHelper.getIPFormat(rawdata, format_info[1], format_info[2])
        elif(data_type==DataType.IPv6):
            return ParseHelper.getIPv6Format(rawdata, format_info[1], format_info[2])
        
        return None # Type isn't specified.

    @staticmethod
    def getNumber(rawdata, start, length) -> int:
        start_padding = 0
        end_padding = 0
        if (start) % 4 != 0:
            start_padding = start % 4
        if (length) % 4 != 0:
            end_padding = 4 - length % 4
        temp_hex = rawdata[(start+start_padding)//4:(start+length+end_padding)//4]

        temp_int = bin(int(temp_hex, 16))
        #print("getNumber({},{},{}) ==> {} ==> {}".format(rawdata, (start+start_padding)//4, (start+length+end_padding)//4, temp_hex, temp_int))
        temp_int = temp_int[2:2+length]

        return int(temp_int, 2)

    @staticmethod
    def getHEX(rawdata, start, length) -> str:
        start_padding = 0
        end_padding = 0
        if (start) % 4 != 0:
            start_padding = start % 4
        if (length) % 4 != 0:
            end_padding = 4 - length % 4
        temp_hex = rawdata[(start+start_padding)//4:(start+length+end_padding)//4]

        temp_int = bin(int(temp_hex, 16))
        #print("getNumber({},{},{}) ==> {} ==> {}".format(rawdata, (start+start_padding)//4, (start+length+end_padding)//4, temp_hex, temp_int))
        temp_int = temp_int[2:2+length]

        return hex(int(temp_int, 2))
        #return rawdata[start:start+length]

    @staticmethod
    def getMACFormat(rawdata, start, length) -> str:
        temp_lst = []
        for i in range(start//4,(start+length)//4,2):
            temp_lst.append(rawdata[i: i+2])
        mac = ":".join(temp_lst)

        return mac.upper()

    @staticmethod
    def getIPFormat(rawdata, start, length) -> str:
        temp_lst = []
        for i in range(start//4,(start+length)//4,2):
            temp_lst.append(str(int(rawdata[i: i+2],16)))
        ip = ".".join(temp_lst)

        return ip

    @staticmethod
    def getIPv6Format(rawdata, start, length) -> str:
        temp_lst = []
        for i in range(start//4,(start+length)//4,2):
            temp_lst.append(rawdata[i: i+2])
        mac = ":".join(temp_lst)

        for i in range(16,1,-1):
            candidate = ("00:"*i)[:-1]
            if mac.find(candidate) > -1:
                mac = mac.replace(candidate,"",1)
                break

        mac = mac.replace("00","0")

        return mac.upper()
