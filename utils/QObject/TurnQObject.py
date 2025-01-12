from .BaseQObject import BaseQObject


class TurnQObject(BaseQObject):
    def __init__(self):
        self.t = 0
        name = "Turn {}".format(self.t)
        super().__init__(name, 10000 / 150)

    def turnAction(self):
        self.time = 100
        self.t += 1
        self.name = "Turn {}".format(self.t)
