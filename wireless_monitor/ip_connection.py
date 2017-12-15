import time

class IPConnection(object):
    def __init__(self, ipHeader, ethHeader, time, attr_names = []):
        self.src = ipHeader.src
        self.dst = ipHeader.dst
        self.proto = ipHeader.protocol
        self.eth_src = ethHeader.src
        self.eth_dst = ethHeader.dst
        self.src_address = ipHeader.src_address
        self.dst_address = ipHeader.dst_address
        self.time_begin = time
        self.time_last = time
        self.data = ipHeader.length
        self.state = None
        self.RX = True

        self.attr_names = []
        self.__populate_core_attr()	

        for attr in attr_names:
	    self.attr_names.append(attr)
            setattr(self, attr, None)

            
    def __populate_core_attr(self):
        self.attr_names.append('src_address')
        self.attr_names.append('RX')
        self.attr_names.append('dst_address')
        self.attr_names.append('proto')
        self.attr_names.append('data')
