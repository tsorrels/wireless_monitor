import socket
import struct
from ctypes import *



class RadiotapHeader(Structure):
    _fields_ = [
        ("version", c_uint8),
        ("pad", c_uint8),
        ("length", c_uint16),
        ("present", c_uint32),
        ]


    def __new__(self, socket_buffer = None):
        return self.from_buffer_copy(socket_buffer)
     
    def __init__(self, socket_buffer = None):
	pass
        
