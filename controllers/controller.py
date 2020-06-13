from PyQt5.QtCore import QObject, pyqtSlot

class Controller(QObject):
    def __init__(self, model):
        super().__init__()

        self._model = model

    @pyqtSlot(str)
    def addRawdata(self, value):
        self._model.rawdata = value

    def showDetail(self, idx):
        return self._model.getDetailDataByIndex(idx)