from wireless_monitor.w_header import WirelessHeader
from wireless_monitor.rt_header import RadiotapHeader
from wireless_monitor.packet_header import PacketHeader
import socket


def read_socket(socket, num_bytes):
    bytes = ''
    while (num_read < num_bytes):
        bytes += socket.recvfrom(num_bytes - len(bytes))

    return bytes
        

# returns 
def parse_headers(socket, packet_type):

    rt_bytes = read_socket(socket, 8)
    rt_header = RadiotapHeader(rt_bytes)

    num_bytes_to_skip = rt.length - 8
    read_socket(socket, num_bytes_to_skip)

    w_bytes = read_socket(socket, 30)
    w_header = WirelessHeader(w_bytes)
    
    
    offset = rt_header.length
    w_header = WirelessHeader(buf[offset:offset + 30])
    
    return (rt_header, w_header)

def parse_headers(raw_buffer):
    size_rt_header = 8
    rt_header = RadiotapHeader(raw_buffer)
    num_rt_bytes = rt_header.length
    offset = num_rt_bytes
    size_w_header = 30
    w_header = None
    
    if len(raw_buffer) >= size_w_header + rt_header.length:
        w_header = WirelessHeader(raw_buffer[offset:offset + 30])

    return (rt_header, w_header)

sniffer = socket.socket(socket.AF_PACKET, socket.SOCK_RAW,
                        socket.ntohs(0x0003))
sniffer.bind(('wlan0mon', 0))

while True:

    raw_buffer = sniffer.recvfrom(65565)[0]
    #print len(raw_buffer)
    (rt_header, w_header) = parse_headers(raw_buffer)
    #w_header = WirelessHeader(raw_buffer[0:30])

    try:
        #print w_header.addr1
        #print w_header.addr2
        #print w_header.addr3
        #print w_header.addr4
        #print w_header.frame_type
        print w_header.subtype

    except:
        pass

