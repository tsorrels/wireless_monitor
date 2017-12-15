import socket
import struct
from ctypes import *


type_map = { 0 : 'Management' , 1 : 'Control' , 2 : 'Data'}
management_subtype_map = { 0 : 'AssociationRequest',
                           1 : 'AssociationResponse',
                           2 : 'ReassociationRequest',
                           3 : 'ReassociationResponse',
                           4 : 'ProbeRequest',
                           5 : 'ProbeResponse',
                           8 : 'Beacon',
                           11: 'Authentication',
                           12: 'Deauthentication' }

control_subtype_map = { 10 : 'BlockACK' , 11 : 'RTS', 13 : 'ACK' }
data_subtype_map = { 0 : 'Data' , 4 : 'NullData' , 8 : 'QoS' , 12: 'NullQoS' }

subtype_type_map = { 0 : management_subtype_map,
                     1 : control_subtype_map,
                     2 : data_subtype_map }



class WirelessHeader(Structure):
    _fields_ = [
        ("frame_control", c_ubyte * 2),
        ("duration_id", c_ubyte * 2),
        ("mac_addr1", c_uint8 * 6),
        ("mac_addr2", c_uint8 * 6),
        ("mac_addr3", c_uint8 * 6),
        ("sequence_control", c_ubyte * 2),
        ("mac_addr4", c_uint8 * 6),
        ]


    def __new__(self, socket_buffer = None):
        return self.from_buffer_copy(socket_buffer)

    def __read_addr__(self, field, attr):
	mac_addr = getattr(self, field)
        OUI = mac_addr[0:3]
        address = mac_addr[3:6]
        
        OUI_string = format(OUI[2],'02x') + ':' + \
                     format(OUI[1],'02x') + ':' + \
                     format(OUI[0],'02x')
        
        addr_string = format(address[2],'02x') + ':' + \
                      format(address[1],'02x') + ':' + \
                      format(address[0],'02x')

        setattr(self, attr, OUI_string + ':' + addr_string)

     
    def __init__(self, socket_buffer = None):
        #self.__read_addr__('mac_addr1', 'addr1')
        #self.__read_addr__('mac_addr2', 'addr2')
        #self.__read_addr__('mac_addr3', 'addr3')
        #self.__read_addr__('mac_addr4', 'addr4')
        #return

        self.version = self.frame_control[0] & 3

        try:             
            frame_type_bits = self.frame_control[0] >> 2 & 3
            self.frame_type = type_map[frame_type_bits]

            subtype_map = subtype_type_map[frame_type_bits]
            subtype_bits = self.frame_control[0] >> 4 & 15
            self.subtype = subtype_map[subtype_bits]

        except KeyError:
            if not self.frame_type:
                self.frame_type = 'Unknown'
            self.subtype = 'Unknown'
            
        
        
        self.addr1 = format(self.mac_addr1[0],'02x') + ':' + \
                     format(self.mac_addr1[1],'02x') + ':' + \
                     format(self.mac_addr1[2],'02x') + ':' + \
                     format(self.mac_addr1[3],'02x') + ':' + \
                     format(self.mac_addr1[4],'02x') + ':' + \
                     format(self.mac_addr1[5],'02x')

        self.addr2 = format(self.mac_addr2[0],'02x') + ':' + \
                     format(self.mac_addr2[1],'02x') + ':' + \
                     format(self.mac_addr2[2],'02x') + ':' + \
                     format(self.mac_addr2[3],'02x') + ':' + \
                     format(self.mac_addr2[4],'02x') + ':' + \
                     format(self.mac_addr2[5],'02x')

        self.addr3 = format(self.mac_addr3[0],'02x') + ':' + \
                     format(self.mac_addr3[1],'02x') + ':' + \
                     format(self.mac_addr3[2],'02x') + ':' + \
                     format(self.mac_addr3[3],'02x') + ':' + \
                     format(self.mac_addr3[4],'02x') + ':' + \
                     format(self.mac_addr3[5],'02x')

        self.addr4 = format(self.mac_addr4[0],'02x') + ':' + \
                     format(self.mac_addr4[1],'02x') + ':' + \
                     format(self.mac_addr4[2],'02x') + ':' + \
                     format(self.mac_addr4[3],'02x') + ':' + \
                     format(self.mac_addr4[4],'02x') + ':' + \
                     format(self.mac_addr4[5],'02x')
