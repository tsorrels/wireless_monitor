
class Extension(object):
    # must explicitly set all components; any can be an empty list
    def __init__(self, threads, hdr_extensions, data_extensions, cmd_extensions):
        self.threads = threads				# must be list
        self.header_extensions = hdr_extensions		# must be list
        self.data_extensions = data_extensions		# must be list
        self.cmd_extensions = cmd_extensions		# must be list
