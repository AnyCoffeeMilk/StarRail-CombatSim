from .BaseQObject import BaseQObject


class PlayerQObject(BaseQObject):
    def __init__(self, name="未設定角色", speed=0):
        super().__init__(name, speed)
        self.e = []
        self.q = []
        self.a = []
        self.enter = []

    def actionForward(self, rate):
        dist = max(self.speed * self.time - 10000 * rate, 0)
        self.time = dist / self.speed
    
    def resetTime(self):
        super().resetTime()
        self.enterAction()

    def enterAction(self):
        for qObjAction in self.enter:
            qObjAction['func'](qObjAction['target'], qObjAction['rate'])

    def turnAction(self, action):
        super().turnAction()
        if action == "E" and self.e != []:
            for qObjAction in self.e:
                qObjAction['func'](qObjAction['target'], qObjAction['rate'])
        if "A" in action and self.q != []:
            for qObjAction in self.a:
                qObjAction['func'](qObjAction['target'], qObjAction['rate'])
    
    def QAction(self):
        for qObjAction in self.q:
            qObjAction['func'](qObjAction['target'], qObjAction['rate'])

    def addAction(self, action_type, qObjAction):
        if action_type == 'enter_action':
            self.enter.append(qObjAction)
        elif action_type == 'e_action':
            self.e.append(qObjAction)
        elif action_type == 'q_action':
            self.q.append(qObjAction)
        elif action_type == 'a_action':
            self.a.append(qObjAction)