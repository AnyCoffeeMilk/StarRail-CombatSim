class BaseQObject():
    def __init__(self, name, speed):
        self.name = name
        self.speed = speed
        self.time = 10000 / speed
    
    def actionForward(self, rate):
        dist = self.speed * self.time - 10000 * rate
        self.time = dist / self.speed
    
    def turnAction(self):
        self.time = 10000 / self.speed