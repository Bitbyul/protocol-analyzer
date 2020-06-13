from common.types import *
from model.dataParser import DataParser

class DefaultLayer:
    format_info_dict = dict()
    info_desc_dict = dict()

    def __init__(self, *args):
        self.info = dict()
        self.info['instance'] = self
        self.info['layer'] = -1
        self.info['rawdata_length'] = -1
        self.info['name'] = "UNKNOWN"
        self.info['detail'] = None

        self.header = None
        self.data = None

        if args:
            self.rawdata = args[0]
            self.info['rawdata_length'] = int(len(args[0])/2)

        if len(args) > 1:
            self.info['name'] = args[1]

        self.upperLayer = None

    def getInfo(self) -> dict:
        info_dict = self.info
        
        if(self.upperLayer):
            info_dict.update({"upperLayer": self.upperLayer.getInfo()})

        return info_dict

    def getName(self) -> str:
        return self.info['name']

    def getDataTypeByKey(self, key):
        try:
            return self.format_info_dict[key][0]
        except (KeyError, NameError, AttributeError):
            return None

    def getDataDetailByKey(self, key):
        try:
            return self.info_desc_dict[key]['detail']
        except (KeyError, NameError, AttributeError):
            return None

    # No More Needed.
    """
    #for detailneededdata (_val)
    def isDetailNeededKey(self, key):
        return key[-4:] == '_val'

    def correctAllDetailNeededKey(self):
        for key in self.format_info_dict:
            if(self.isDetailNeededKey(key)):
                try:
                    self.info[key[:-4]] = self.info_desc_dict[key[:-4]][self.info[key]]
                except KeyError:
                    pass
    """
    def getDesc(self, key, value):
        descDetail = ""
        try:
            matchType = self.info_desc_dict[key]['desctype']
            if(matchType==DescType.MATCHWHOLE):
                if(value in self.info_desc_dict[key]):
                    descDetail = self.info_desc_dict[key][value]
                else:
                    descDetail = self.info_desc_dict[key]['default']
            elif(matchType==DescType.MATCHFUNCTION):
                matchFunc = self.info_desc_dict[key]['func']
                resultValue = matchFunc(value)
                if(resultValue in self.info_desc_dict[key]):
                    descDetail = self.info_desc_dict[key][resultValue]
                else:
                    descDetail = self.info_desc_dict[key]['default']
            elif(matchType==DescType.NUMBER):
                descDetail = str(value)
            elif(matchType==DescType.BYTES):
                descDetail = str(value) + " bytes"
            elif(matchType==DescType.BYTESMUL4):
                descDetail = str(value*4) + " bytes"
            elif(matchType==DescType.MATCHFROMIPPROTOCOL):
                descDetail = DataParser.getIPProtocolNameByNum(value)
            elif(matchType==DescType.MATCHFROMSERVICE):
                descDetail += str(value) + " // "
                serviceName = DataParser.getServiceName(value,self.info['name'])
                if serviceName[1]:
                    descDetail += serviceName[1]
                else:
                    descDetail += serviceName[0]
            elif(matchType==DescType.FUNCTIONRESULT):
                descDetail = DataParser.getIPProtocolNameByNum(value)
                func = self.info_desc_dict[key]['func']
                descDetail = func(value)
                

            if('headtext' in self.info_desc_dict[key]):
                descDetail = self.info_desc_dict[key]['headtext'] + " " + descDetail
            if('tailtext' in self.info_desc_dict[key]):
                descDetail += " " + self.info_desc_dict[key]['tailtext']
            return descDetail
        except (KeyError, NameError, AttributeError):
            return None