from utils.QObject.BaseQObject import BaseQObject
from utils.QObject.TurnQObject import TurnQObject
from utils.CombatQueue import CombatQueue

q = CombatQueue(
    [
        BaseQObject("黃泉", 122),
        BaseQObject("花火", 157),
        BaseQObject("椒丘", 158),
        BaseQObject("符玄", 150),
        TurnQObject(),
    ]
)

q.getQObject("花火").actionForward(0.4)
q.getQObject("椒丘").actionForward(0.4)

q.getQueue()

while input() != "0":
    q.forward()
    q.getQueue()
    q.getHead().turnAction()
