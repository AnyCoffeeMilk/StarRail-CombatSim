class BaseQObject:
    def __init__(self, name, speed, e=None, q=None):
        self.name = name
        self.speed = speed
        self.time = 10000 / speed
        self.e = e
        self.q = q

    def turnAction(self, action):
        self.time = 10000 / self.speed
