# TCP/IP 5th layer - Application Layer (The last layer)
from model.layers.DefaultLayer import *
from common.types import *

class DefaultApplicationLayer(DefaultLayer):
    def __init__(self, *args):
        super().__init__(*args)

        self.info['layer'] = 5
