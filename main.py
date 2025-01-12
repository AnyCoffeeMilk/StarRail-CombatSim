import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QGroupBox,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QLineEdit,
    QComboBox,
    QFormLayout,
    QDialog,
    QDialogButtonBox,
)
from PyQt5.QtCore import Qt
from utils.QObject.PlayerQObject import PlayerQObject
from utils.QObject.TurnQObject import TurnQObject
from utils.CombatQueue import CombatQueue


class ActionDialog(QDialog):
    def __init__(self, parent=None, targets=None):
        super().__init__(parent)
        self.setWindowTitle("添加行為")

        self.layout = QFormLayout()

        # Create inputs
        self.type_input = QLineEdit()
        self.target_input = QComboBox()  # Use QComboBox for the target
        self.percentage_input = QLineEdit()

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
        return (
            self.type_input.text(),
            self.target_input.currentText(),  # Get the selected item
            self.percentage_input.text(),
        )



class CombatQueueUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize CombatQueue with 5 items
        self.q = CombatQueue(
            [
                PlayerQObject("黃泉", 122),
                PlayerQObject("花火", 157),
                PlayerQObject("椒丘", 158),
                PlayerQObject("符玄", 150),
                TurnQObject(),
            ]
        )

        self.setWindowTitle("星鐵排軸模擬器")
        self.setGeometry(100, 100, 500, 800)

        # Main widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layouts
        self.main_layout = QVBoxLayout()
        self.queue_layout = QVBoxLayout()
        self.edit_layout = QHBoxLayout()

        # Queue display
        self.queue_label = QLabel("行動軸:")
        self.queue_list = QListWidget()

        # Force the queue display to fit at least 8 rows in height
        row_height = 20
        self.queue_list.setMinimumHeight(row_height * 8 + 2 * self.queue_list.frameWidth())

        self.queue_layout.addWidget(self.queue_label)
        self.queue_layout.addWidget(self.queue_list)

        # Editable fields for each PlayerQObject
        self.objects_form = QFormLayout()
        self.edit_boxes = {}  # To store input fields for each object

        for obj in self.q.getQueue():
            if not isinstance(obj, TurnQObject):
                obj_group = QGroupBox(f"{obj.name}")
                obj_layout = QVBoxLayout()

                # Name field
                name_input = QLineEdit(obj.name)
                name_input.textChanged.connect(
                    lambda text, o=obj: self.update_name(o, text)
                )
                name_form = QFormLayout()
                name_form.addRow("名稱:", name_input)
                obj_layout.addLayout(name_form)

                # Speed field
                speed_input = QLineEdit(str(obj.speed))
                speed_input.textChanged.connect(
                    lambda text, o=obj: self.update_speed(o, text)
                )
                speed_form = QFormLayout()
                speed_form.addRow("速度:", speed_input)
                obj_layout.addLayout(speed_form)

                # E Button
                e_button = QPushButton("E")
                e_button.clicked.connect(lambda _, o=obj: self.handle_e_action(o))
                e_button.setMaximumWidth(40)
                
                # Q Button
                q_button = QPushButton("Q")
                q_button.clicked.connect(lambda _, o=obj: self.handle_q_action(o))
                q_button.setMaximumWidth(40)
                
                # A Button
                a_button = QPushButton("A")
                a_button.clicked.connect(lambda _, o=obj: self.handle_a_action(o))
                a_button.setMaximumWidth(40)

                button_layout = QHBoxLayout()
                button_layout.addWidget(e_button)
                button_layout.addWidget(q_button)
                button_layout.addWidget(a_button)
                obj_layout.addLayout(button_layout)

                # E Actions
                e_layout = QHBoxLayout()
                e_label = QLabel("E 行為:")
                e_button = QPushButton("+")
                e_button.setMaximumWidth(40)
                e_button.clicked.connect(lambda _, o=obj: self.add_action(o, "E"))
                e_layout.addWidget(e_label)
                e_layout.addWidget(e_button)
                obj_layout.addLayout(e_layout)

                e_actions_list = QListWidget()
                obj_layout.addWidget(e_actions_list)

                # Q Actions
                q_layout = QHBoxLayout()
                q_label = QLabel("Q 行為:")
                q_button = QPushButton("+")
                q_button.setMaximumWidth(40)
                q_button.clicked.connect(lambda _, o=obj: self.add_action(o, "Q"))
                q_layout.addWidget(q_label)
                q_layout.addWidget(q_button)
                obj_layout.addLayout(q_layout)

                q_actions_list = QListWidget()
                obj_layout.addWidget(q_actions_list)

                # A Actions
                a_layout = QHBoxLayout()
                a_label = QLabel("A 行為:")
                a_button = QPushButton("+")
                a_button.setMaximumWidth(40)
                a_button.clicked.connect(lambda _, o=obj: self.add_action(o, "A"))
                a_layout.addWidget(a_label)
                a_layout.addWidget(a_button)
                obj_layout.addLayout(a_layout)

                a_actions_list = QListWidget()
                obj_layout.addWidget(a_actions_list)

                # Store references to the lists
                self.edit_boxes[obj] = {
                    "name": name_input,
                    "speed": speed_input,
                    "e_actions": e_actions_list,
                    "q_actions": q_actions_list,
                    "a_actions": a_actions_list,
                }

                obj_group.setLayout(obj_layout)
                self.edit_layout.addWidget(obj_group)

        # Add layouts to main layout
        self.main_layout.addLayout(self.queue_layout)
        self.main_layout.addLayout(self.edit_layout)

        # Set main layout
        self.central_widget.setLayout(self.main_layout)

        # Initialize queue display
        self.update_queue_display()

    def update_name(self, obj, name):
        """Update the name of a PlayerQObject."""
        obj.name = name
        self.update_queue_display()

    def update_speed(self, obj, speed):
        """Update the speed of a PlayerQObject."""
        try:
            obj.speed = int(speed)
            self.update_queue_display()
        except ValueError:
            print("Invalid speed value")

    def handle_e_action(self, obj, target_input, percentage_input):
        """Handle the E action for a specific PlayerQObject."""
        try:
            self.q.getHead().turnAction("A")
            if target_input.currentText() != "":
                target = target_input.currentText()
                percentage = float(percentage_input.text())
                self.q.getQObject(target).actionForward(percentage)
            self.q.forward()
            if isinstance(self.q.getHead(), TurnQObject):
                self.q.getHead().turnAction()
                self.q.forward()
            self.update_queue_display()
        except (ValueError, AttributeError):
            print(f"Invalid input for E action on {obj.name}")

    def handle_q_action(self, obj, target_input, percentage_input):
        """Handle the Q action for a specific PlayerQObject."""
        try:
            if target_input.currentText() != "":
                target = target_input.currentText()
                percentage = float(percentage_input.text())
                self.q.getQObject(target).actionForward(percentage)
            self.update_queue_display()
        except (ValueError, AttributeError):
            print(f"Invalid input for Q action on {obj.name}")

    def handle_action(self):
        """Handle the Q action for a specific PlayerQObject."""
        self.q.getHead().turnAction("A")
        self.q.forward()
        if isinstance(self.q.getHead(), TurnQObject):
            self.q.getHead().turnAction()
            self.q.forward()
        self.update_queue_display()

    def add_action(self, obj, action_type):
        """Add an action to a specific PlayerQObject."""
        # Generate a list of target names from the queue
        targets = [o.name for o in self.q.getQueue() if isinstance(o, PlayerQObject)]
        targets.insert(0, '')
        dialog = ActionDialog(self, targets=targets)
        if dialog.exec_() == QDialog.Accepted:
            action_data = dialog.get_action_data()
            if action_type == "E":
                self.edit_boxes[obj]["e_actions"].addItem(
                    f"{action_data[0]}, {action_data[1]}, {action_data[2]}"
                )
            elif action_type == "Q":
                self.edit_boxes[obj]["q_actions"].addItem(
                    f"{action_data[0]}, {action_data[1]}, {action_data[2]}"
                )
            elif action_type == "A":
                self.edit_boxes[obj]["a_actions"].addItem(
                    f"{action_data[0]}, {action_data[1]}, {action_data[2]}"
                )

    def update_queue_display(self):
        """Update the queue display based on the current state of the CombatQueue."""
        self.queue_list.clear()
        queue_state = ["{} (行動值: {:.1f})".format(x.name, x.time) for x in self.q.getQueue()]
        for obj in queue_state:
            self.queue_list.addItem(obj)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = CombatQueueUI()
    main_window.show()
    sys.exit(app.exec_())
