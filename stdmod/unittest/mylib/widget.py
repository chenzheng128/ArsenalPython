class Widget:
    def __init__(self, name):
        self.x = 50
        self.y = 50
        pass

    def resize(self, x, y):
        self.x = x
        self.y = y

    def size(self):
        return self.x, self.y

    def dispose(self):
        pass
