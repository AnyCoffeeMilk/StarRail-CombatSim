class BaseQObject:
    def __init__(self, name="", speed=0):
        self.name = name
        self.speed = speed
        self.updateTime()
    
    def updateTime(self):
        if self.speed == 0:
            self.time = -1
        else:
            self.time = 10000 / self.speed
    
    def resetTime(self):
        self.updateTime()

    def turnAction(self, action):
        self.updateTime()
