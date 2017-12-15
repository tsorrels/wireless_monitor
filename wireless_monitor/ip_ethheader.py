import socket
import struct
from ctypes import *


class EthHeader(Structure):
    _fields_ = [
        ("ether_dhost", c_uint8 * 6),
        ("ether_shost", c_uint8 * 6),
        ("ether_type", c_uint16)
        ]


    def __new__(self, socket_buffer = None):
        return self.from_buffer_copy(socket_buffer)
     
    def __init__(self, socket_buffer = None):
        self.src = format(self.ether_shost[0],'02x') + ':' + \
                   format(self.ether_shost[1],'02x') + ':' + \
                   format(self.ether_shost[2],'02x') + ':' + \
                   format(self.ether_shost[3],'02x') + ':' + \
                   format(self.ether_shost[4],'02x') + ':' + \
                   format(self.ether_shost[5],'02x')

        self.dst = format(self.ether_dhost[0],'02x') + ':' + \
                   format(self.ether_dhost[1],'02x') + ':' + \
                   format(self.ether_dhost[2],'02x') + ':' + \
                   format(self.ether_dhost[3],'02x') + ':' + \
                   format(self.ether_dhost[4],'02x') + ':' + \
                   format(self.ether_dhost[5],'02x')

        
