class CombatQueue:
    def __init__(self, qObj_list):
        self.q = qObj_list
        self.sortQueue()

    def getQueue(self, noSort=False):
        if not noSort:
            self.sortQueue()
        return self.q

    def sortQueue(self):
        self.q.sort(key=lambda qObj: qObj.time)

    def getQObject(self, name):
        for i in self.q:
            if i.name == name:
                return i

    def getHead(self):
        self.sortQueue()
        return self.q[0]

    def forward(self):
        self.sortQueue()
        head_t = self.getHead().time
        for i in self.q:
            i.time -= head_t
