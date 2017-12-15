import importlib
import traceback
import signal
import threading
import os
import struct
import socket
import time
import curses
import getopt
import sys
import socket
import fcntl
import struct
from ip_connection import IPConnection
from ip_header import IP
from display_headers import *
from display_item import *
from logwriter import LogWriter


class GlobalState(object):
    def __init__(self, namespace):

        self.logwriter = LogWriter()
        self.logwriter.add_log('error', './error_log.txt')        
        
	self.all_connections = []
	self.all_lock = threading.Lock()
        self.udp_connections = []
        self.udp_lock = threading.Lock()
        self.tcp_connections = []
        self.tcp_lock = threading.Lock()
        self.icmp_connections = []
        self.icmp_lock = threading.Lock()

        self.connections_map = {
            socket.IPPROTO_ICMP : (self.icmp_connections, self.icmp_lock),
            socket.IPPROTO_UDP : (self.udp_connections, self.udp_lock),
            socket.IPPROTO_TCP : (self.tcp_connections, self.tcp_lock) }

        self.cmd_extensions = []
        self.header_extensions = []
        self.data_extensions = []
        self.run_threads = []

        self.exit_functions = []
        
        self.display_headers = default_headers

        self.permiscuous = False
        self.interface = None
        
        args_dictionary = vars(namespace)
        
        self.interface = args_dictionary['interface']
        
        if 'p' in args_dictionary:
            self.permiscuous = True
                        
        # load modules
        for mod in args_dictionary['args']:
            self.__load_mod(mod)

        self.host_address = self.__get_ip_address(self.interface)
            
            

    def __load_mod(self, mod):
        try:

            if len(mod) > 3 and mod[-3:] == '.py':
                mod = mod[0:-3]
            
            importlib.import_module(mod)
            extension = sys.modules[str(mod)].extension

            #add commands
            for cmd in extension.cmd_extensions:
                self.cmd_extensions.append(cmd)
            
            #add headers
            for header in extension.header_extensions:
                self.display_headers.append(header)
                
            #add connection data
            for data in extension.data_extensions:
                self.data_extensions.append(data)
            
            #add execution threads             
            for runnable in extension.threads:
                self.run_threads.append(runnable)

            #add exit function
            self.exit_functions.append(sys.modules[str(mod)].exit)
                
        except KeyError as e:
            self.logwriter.write('error', "Key error")
            
        
        except Exception as e:
            self.logwriter.write('error', 'Other exception, ' + mod + str(e))

    # taken from
    # https://stackoverflow.com/questions/24196932/
    # how-can-i-get-the-ip-address-of-eth0-in-python
    def __get_ip_address(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])


    def __parse_line(self, line):
        words = line.split()
        ip_src = words[0]
        ip_dst = words[1]
        if ip_dst == '->':
            ip_dst = words[2]

        return (ip_src, ip_dst)
        
        
    def find_connection(self, data):
        (ip_src, ip_dst) = self.__parse_line(data)
        with self.all_lock:            
            for connection in self.all_connections:
                if ip_src == connection.src_address and \
                   ip_dst == connection.dst_address:
                    return connection

        self.logwriter.write('error', 'did not find connection in controller: ' + data + connection.src_address + connection.dst_address + '\n')
        return #None
    
