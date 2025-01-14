from PyQt5.QtWidgets import (
    QLineEdit,
    QComboBox,
    QFormLayout,
    QDialog,
    QDialogButtonBox,
)
from ..QObjAction import QObjActionTemplates

class ActionDialog(QDialog):
    def __init__(self, parent=None, targets=None):
        super().__init__(parent)
        self.setWindowTitle("添加行為")

        self.layout = QFormLayout()

        # Create inputs
        self.type_input = QComboBox()
        self.target_input = QComboBox()  # Use QComboBox for the target
        self.percentage_input = QLineEdit()

        self.type_input.addItem("")
        for qObjAction in QObjActionTemplates:
            self.type_input.addItem(qObjAction["name"])

        # Populate the target dropdown
        if targets:
            self.target_input.addItems(targets)

        # Add inputs to the layout
        self.layout.addRow("類型:", self.type_input)
        self.layout.addRow("目標:", self.target_input)
        self.layout.addRow("百分比:", self.percentage_input)

        # Dialog buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)

    def get_action_data(self):
        """Return the data entered in the dialog."""
        rate = self.percentage_input.text()
        if "%" in rate:
            rate = float(rate.strip("%")) / 100
        else:
            rate = float(rate)
        return (
            self.type_input.currentText(),
            self.target_input.currentText(),  # Get the selected item
            rate,
        )