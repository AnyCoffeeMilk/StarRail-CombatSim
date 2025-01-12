from .BaseQObject import BaseQObject


class PlayerQObject(BaseQObject):
    def __init__(self, name, speed, e=None, q=None):
        self.name = name
        self.speed = speed
        self.time = 10000 / speed
        self.e = e
        self.q = q

    def actionForward(self, rate):
        dist = max(self.speed * self.time - 10000 * rate, 0)
        self.time = dist / self.speed

    def turnAction(self, action):
        self.time = 10000 / self.speed
        if "E" in action and self.e != None:
            self.e()
        if "Q" in action and self.q != None:
            self.q()
