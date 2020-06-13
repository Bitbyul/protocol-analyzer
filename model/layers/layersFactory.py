import model.layers.linkLayers
from model.layers.linkLayers import *

class LayersFactory:
    @staticmethod
    def createProtocolByRawdata(rawdata):
        return Ethernet(rawdata)