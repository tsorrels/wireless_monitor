
class HeaderItem(object):
    def __init__(self, text, length, offset = None):
        self.text = text	# must be string
        self.length = length	# integer representing max character output for item
        self.offset = offset	# not used


default_headers = [ HeaderItem("SRCIP", 15),
                    HeaderItem("RX", 4),
                    HeaderItem("DSTIP", 15),
                    HeaderItem("PROTO", 5),
                    HeaderItem("DATA", 8) ]

