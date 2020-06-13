import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from common.types import *

form_class = uic.loadUiType("views/qt/MainForm.ui")[0]

class DetailModel(QStandardItemModel):
    def __init__(self, data):
        QStandardItemModel.__init__(self)

        ignore_key_list = ["instance","name","upperLayer","protocols","rawdata_length","layer"]

        j = 0
        while True:
            item = QStandardItem("Layer {}: {}".format(data["layer"], data["name"]))
            item.setFont(QFont("맑은 고딕", 14, QFont.Bold))
            self.setItem(j, 0, item)
            self.setItem(j, 1, QStandardItem(""))
            self.setItem(j, 2, QStandardItem(""))
            
            if not data['instance'].format_info_dict: # Unknown Protocol
                if(hasattr(data['instance'], 'rawdata') and data['instance'].rawdata != ""):
                    child_key = QStandardItem('rawdata')
                    child_value = QStandardItem(data['instance'].rawdata)
                    item.appendRow([child_key, child_value])
                break

            for key, value in data.items():
                if key=='detail': 
                    self.setItem(j, 2, QStandardItem(value))
                elif not (key in ignore_key_list):

                    valueType = data["instance"].getDataTypeByKey(key)
                    keyDetail = data["instance"].getDataDetailByKey(key)
                    if(keyDetail):
                        child_key = QStandardItem(keyDetail)
                    else:
                        child_key = QStandardItem(key)

                    desc_content = data["instance"].getDesc(key, value)

                    if(isinstance(desc_content, dict)):
                        # For dictionary type. HARD CODING TEMPORARY. TODO: Need to classify
                        child_desc = QStandardItem(desc_content['DESC'])
                        for key_desc, value_desc in desc_content.items():
                            if key_desc == "DESC": continue
                            child_child_key = QStandardItem(key_desc)
                            child_child_value = QStandardItem(value_desc[0])
                            child_child_desc = QStandardItem(value_desc[1])

                            child_child_key.setFont(QFont("맑은 고딕", 12))
                            child_child_value.setFont(QFont("맑은 고딕", 10))
                            child_child_desc.setFont(QFont("맑은 고딕", 10))

                            child_key.appendRow([child_child_key, child_child_value, child_child_desc])
                    else:
                        child_desc = QStandardItem(data["instance"].getDesc(key, value))
                    
                    if(valueType == DataType.NUM):
                        child_value = QStandardItem(str(hex(value)))
                    elif(valueType == DataType.HEX):
                        child_value = QStandardItem(str(hex(int(value,16))))
                    else:
                        child_value = QStandardItem(str(value))

                    child_key.setForeground(QBrush(QColor("#123456")))
                    child_value.setFont(QFont("맑은 고딕", 13))
                    child_desc.setFont(QFont("맑은 고딕", 13))

                    item.appendRow([child_key, child_value, child_desc])
                    #child_key.appendRow(child_value)

            if not ("upperLayer" in data): break
            data = data['upperLayer']
            j+=1

class MainForm(QMainWindow, form_class):
    def __init__(self, model, controller):
        super().__init__()

        self._model = model
        self._controller = controller
        self.setupUi(self)

        self.table = self.tableDataList
        self.detailTree = self.treeDetailView

        self.btnAddRawData.clicked.connect(self.btnAddRawData_clicked)
        self._model.rawdata_added.connect(self.onRawDataAdded)

        self.table.itemClicked.connect(self.tableDataList_clicked)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.Stretch)
        
        self.detailTree.collapsed.connect(self.correctTreeViewSize)
        self.detailTree.expanded.connect(self.correctTreeViewSize)

    def btnAddRawData_clicked(self):
        text, ok = QInputDialog.getText(self, 'Protocol Analyzer :: Add Data', 'Enter Ethernet Frame Raw Data[ex) 001e902ec7... | 00 1e 90 2e c7...]:                            ')
        if ok:
            text = str(text).replace(" ", "")
            print("Frame Data: {}".format(text))
            self._controller.addRawdata(text)
    
    def tableDataList_clicked(self,clicked):
        data_dict = self._controller.showDetail(clicked.row())

        # set tree view model from protocol info dict
        detailModel = DetailModel(data_dict)
        self.detailTree.setModel(detailModel)
        self.correctTreeViewSize()

    def correctTreeViewSize(self):
        self.detailTree.resizeColumnToContents(0)
        self.detailTree.resizeColumnToContents(1)
        self.detailTree.resizeColumnToContents(2)

    @pyqtSlot(dict)
    def onRawDataAdded(self, value):
        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)

        for i in range(self.table.columnCount()):
            self.table.setItem(rowPosition,i,QTableWidgetItem("-"))

        self.table.setItem(rowPosition,0,QTableWidgetItem(value['src_mac_addr']))
        self.table.setItem(rowPosition,1,QTableWidgetItem(value['dst_mac_addr']))
        if(value['Type'] == 0x0800): # IP HARD CODING Temporary... TODO: Make getter methods
            self.table.setItem(rowPosition,2,QTableWidgetItem(value['upperLayer']['src_ip_addr']))
            self.table.setItem(rowPosition,3,QTableWidgetItem(value['upperLayer']['dst_ip_addr']))
        elif(value['Type'] == 0x0806): # ARP Hard CODING Temporary... TODO
            self.table.setItem(rowPosition,2,QTableWidgetItem(value['upperLayer']['src_proto_addr']))
            self.table.setItem(rowPosition,3,QTableWidgetItem(value['upperLayer']['dst_proto_addr']))
        elif(value['Type'] == 0x86dd): # IPv6 Hard CODING Temporary... TODO
            self.table.setItem(rowPosition,2,QTableWidgetItem(value['upperLayer']['src_ip_addr']))
            self.table.setItem(rowPosition,3,QTableWidgetItem(value['upperLayer']['dst_ip_addr']))
        self.table.setItem(rowPosition,4,QTableWidgetItem(str(value['rawdata_length'])))
        self.table.setItem(rowPosition,5,QTableWidgetItem(str(value['protocols'])))
        detail = value['detail']
        tempInfo = value
        while True:
            if not ("upperLayer" in tempInfo): break
            tempInfo = tempInfo['upperLayer']
            if 'detail' in tempInfo:
                if not tempInfo['detail']: break
                detail = tempInfo['detail']

        self.table.setItem(rowPosition,6,QTableWidgetItem(detail))
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.Stretch)