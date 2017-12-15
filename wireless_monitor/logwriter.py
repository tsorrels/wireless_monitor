import threading

relative_path = './logs/'

class LogWriter(object):
    def __init__(self):
        self.handles = {}
        self.lock = threading.Lock()
        
    def add_log(self, alias, filename):
        with self.lock:
            handle = open(relative_path + filename, 'a')
            logHandle = LogHandle(alias, handle)
            self.handles[alias] = logHandle

    def write(self, handle, message):
        try:
            logHandle = self.handles[handle]
            with logHandle.lock:
                logHandle.handle.write(message)

        except KeyError as E:
            pass

            


class LogHandle(object):
    def __init__(self, alias, handle):
        self.alias = alias
        self.handle = handle
        self.lock = threading.Lock()

        
