
class PacketHeader(object):
    def __init__(self, rt_header, w_header, ip_header):
        self.rt_header = rt_header
        self.w_header = w_header
        self.ip_header = ip_header
