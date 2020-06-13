import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from model.model import Model
from controllers.controller import Controller
from views import *

class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.model = Model()
        self.controller = Controller(self.model)
        self.main_view = mainView.MainForm(self.model, self.controller)
        self.main_view.show()

def initialize():
    app = App(sys.argv)
    sys.exit(app.exec_())

if __name__ == "__main__":
    initialize()