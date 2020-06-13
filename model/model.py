from PyQt5.QtCore import QObject, pyqtSignal
from model.dataParser import DataParser
from model.layers.layersFactory import LayersFactory

class Model(QObject):
    rawdata_added = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self._rawdataList = list()

    @property
    def rawdata(self):
        return self._rawdata

    @rawdata.setter
    def rawdata(self, value):
        info_dict = LayersFactory.createProtocolByRawdata(value).getInfo()
        info_dict.update({'protocols': DataParser.getProtocolNameListFromProtocolInfo(info_dict)})
        if info_dict:
            self._rawdataList.append(info_dict)
            #self.rawdata_added.emit(self._rawdata)
            print(self._rawdataList[-1])
            self.rawdata_added.emit(info_dict)

    def getDetailDataByIndex(self, idx):
        return self._rawdataList[idx]
"""
    @property
    def rawdataList(self):
        return self._rawDataList
    
    def addRawData(self, rawdata):
        self._rawdataList.append(rawdata)
        self.rawdata_added(_rawdataList)
"""