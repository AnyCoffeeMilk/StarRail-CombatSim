def forwardAction(tgt_qObj, rate):
    tgt_qObj.actionForward(rate)

QObjActionTemplates = [
    {
        "name": "拉條",
        "func": forwardAction,
        "target": None,
        "rate": None,
    },
    {
        "name": "加速",
        "func": forwardAction,
        "target": None,
        "rate": None,
    },
]