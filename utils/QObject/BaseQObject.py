class BaseQObject:
    def __init__(self, name, speed):
        self.name = name
        self.speed = speed
        self.time = 10000 / speed

    def turnAction(self, action):
        self.time = 10000 / self.speed
