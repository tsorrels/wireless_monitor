
class DisplayItem(object):
    def __init__(self, data):
        self.data = data

    def display(self):
        return str(self.data)
