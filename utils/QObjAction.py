def forwardAction(tgt_qObj, rate):
    tgt_qObj.actionForward(rate)

QObjActionTemplates = [
    {
        "type": "拉條",
        "func": forwardAction,
        "target": None,
        "rate": None,
    },
    {
        "type": "加速",
        "func": forwardAction,
        "target": None,
        "rate": None,
    },
]