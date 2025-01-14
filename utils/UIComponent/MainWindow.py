from PyQt5.QtWidgets import (
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
)
from ..QObject.PlayerQObject import PlayerQObject
from ..QObject.TurnQObject import TurnQObject
from ..CombatQueue import CombatQueue
from ..QObjAction import QObjActionTemplates

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize CombatQueue with 5 items
        self.q = CombatQueue(
            [
                PlayerQObject(),
                PlayerQObject(),
                PlayerQObject(),
                PlayerQObject(),
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

        # Queue  display
        queue_label_layout = QHBoxLayout()
        queue_label = QLabel("行動軸:")
        self.queue_button = QPushButton("開始模擬")
        self.queue_button.setMaximumWidth(80)
        self.queue_button.clicked.connect(self.handle_restart)
        queue_label_layout.addWidget(queue_label)
        queue_label_layout.addWidget(self.queue_button)

        self.queue_list = QListWidget()
        row_height = 20
        self.queue_list.setMinimumHeight(
            row_height * 8 + 2 * self.queue_list.frameWidth()
        )

        self.queue_layout.addLayout(queue_label_layout)
        self.queue_layout.addWidget(self.queue_list)

        # Editable fields for each PlayerQObject
        self.objects_form = QFormLayout()
        self.edit_boxes = {}  # To store input fields for each object

        for QObj in self.q.getQueue():
            if isinstance(QObj, PlayerQObject):
                obj_group = QGroupBox()
                obj_layout = QVBoxLayout()

                # Name field
                name_input = QLineEdit()
                name_input.textChanged.connect(
                    lambda text, o=QObj: self.update_name(o, text)
                )
                name_form = QFormLayout()
                name_form.addRow("角色:", name_input)
                obj_layout.addLayout(name_form)

                # Speed field
                speed_input = QLineEdit()
                speed_form = QFormLayout()
                speed_form.addRow("速度:", speed_input)
                obj_layout.addLayout(speed_form)

                # E Button
                e_button = QPushButton("E")
                e_button.clicked.connect(lambda _, o=QObj: self.handle_e_action(o))
                e_button.setMaximumWidth(40)

                # Q Button
                q_button = QPushButton("Q")
                q_button.clicked.connect(lambda _, o=QObj: self.handle_q_action(o))
                q_button.setMaximumWidth(40)

                # A Button
                a_button = QPushButton("A")
                a_button.clicked.connect(lambda _, o=QObj: self.handle_a_action(o))
                a_button.setMaximumWidth(40)
                button_layout = QHBoxLayout()
                button_layout.addWidget(e_button)
                button_layout.addWidget(q_button)
                button_layout.addWidget(a_button)
                obj_layout.addLayout(button_layout)

                # Enter Actions
                enter_layout = QHBoxLayout()
                enter_label = QLabel("進場行為:")
                enter_button = QPushButton("+")
                enter_button.setMaximumWidth(40)
                enter_button.clicked.connect(lambda _, o=QObj: self.add_action(o, "Enter"))
                enter_layout.addWidget(enter_label)
                enter_layout.addWidget(enter_button)
                obj_layout.addLayout(enter_layout)

                enter_actions_list = QListWidget()
                enter_actions_list.setMaximumHeight(
                    row_height * 4 + 2 * self.queue_list.frameWidth()
                )
                obj_layout.addWidget(enter_actions_list)

                # E Actions
                e_layout = QHBoxLayout()
                e_label = QLabel("E 行為:")
                e_button = QPushButton("+")
                e_button.setMaximumWidth(40)
                e_button.clicked.connect(lambda _, o=QObj: self.add_action(o, "E"))
                e_layout.addWidget(e_label)
                e_layout.addWidget(e_button)
                obj_layout.addLayout(e_layout)

                e_actions_list = QListWidget()
                e_actions_list.setMaximumHeight(
                    row_height * 4 + 2 * self.queue_list.frameWidth()
                )
                obj_layout.addWidget(e_actions_list)

                # Q Actions
                q_layout = QHBoxLayout()
                q_label = QLabel("Q 行為:")
                q_button = QPushButton("+")
                q_button.setMaximumWidth(40)
                q_button.clicked.connect(lambda _, o=QObj: self.add_action(o, "Q"))
                q_layout.addWidget(q_label)
                q_layout.addWidget(q_button)
                obj_layout.addLayout(q_layout)

                q_actions_list = QListWidget()
                q_actions_list.setMaximumHeight(
                    row_height * 4 + 2 * self.queue_list.frameWidth()
                )
                obj_layout.addWidget(q_actions_list)

                # A Actions
                a_layout = QHBoxLayout()
                a_label = QLabel("A 行為:")
                a_button = QPushButton("+")
                a_button.setMaximumWidth(40)
                a_button.clicked.connect(lambda _, o=QObj: self.add_action(o, "A"))
                a_layout.addWidget(a_label)
                a_layout.addWidget(a_button)
                obj_layout.addLayout(a_layout)

                a_actions_list = QListWidget()
                a_actions_list.setMaximumHeight(
                    row_height * 4 + 2 * self.queue_list.frameWidth()
                )
                obj_layout.addWidget(a_actions_list)

                # Store references to the lists
                self.edit_boxes[QObj] = {
                    "name": name_input,
                    "speed": speed_input,
                    "enter_actions": enter_actions_list,
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

    def handle_e_action(self, QObj):
        """Handle the E action for a specific PlayerQObject."""
        try:
            self.q.getHead().turnAction("E")
            self.q.forward()
            if isinstance(self.q.getHead(), TurnQObject):
                self.q.getHead().turnAction()
                self.q.forward()
            self.update_queue_display()
        except (ValueError, AttributeError):
            print(f"Invalid input for E action on {QObj.name}")

    def handle_q_action(self, QObj):
        """Handle the Q action for a specific PlayerQObject."""
        try:
            QObj.QAction()
            self.update_queue_display()
        except (ValueError, AttributeError):
            print(f"Invalid input for Q action on {QObj.name}")

    def handle_a_action(self, QObj):
        """Handle the A action for a specific PlayerQObject."""
        self.q.getHead().turnAction("A")
        self.q.forward()
        if isinstance(self.q.getHead(), TurnQObject):
            self.q.getHead().turnAction()
            self.q.forward()
        self.update_queue_display()
    
    def handle_restart(self):
        self.queue_button.setText("重置")
        for qObj in self.q.getQueue():
            if isinstance(qObj, PlayerQObject):
                qObj.name = self.edit_boxes[qObj]["name"].text()
                qObj.speed = float(self.edit_boxes[qObj]["speed"].text())
            qObj.resetTime()
        self.update_queue_display()

    def add_action(self, QObj, action_type):
        """Add an action to a specific PlayerQObject."""
        # Generate a list of target names from the queue
        targets = [o.name for o in self.q.getQueue() if isinstance(o, PlayerQObject)]
        targets.insert(0, "")
        dialog = ActionDialog(self, targets=targets)
        if dialog.exec_() == QDialog.Accepted:
            action_data = dialog.get_action_data()
            for qObjAction in QObjActionTemplates:
                if qObjAction["name"] == action_data[0]:
                    target_data = self.q.getQObject(action_data[1])
                    rate_data = float(action_data[2])
                    QObj.addAction(
                        action_type,
                        {
                            "name": qObjAction["name"],
                            "func": lambda target=target_data, rate=rate_data: qObjAction["func"](target, rate),
                            "target": action_data[1],
                            "rate": action_data[2],
                        },
                    )
            self.update_action_list_display()

    def update_action_list_display(self):
        for qObj in self.q.getQueue():
            if isinstance(qObj, PlayerQObject):
                self.edit_boxes[qObj]["enter_actions"].clear()
                self.edit_boxes[qObj]["e_actions"].clear()
                self.edit_boxes[qObj]["q_actions"].clear()
                self.edit_boxes[qObj]["a_actions"].clear()
                for qObjAction in qObj.enter:
                    self.edit_boxes[qObj]["enter_actions"].addItem(
                        f"{qObjAction['name']}, {qObjAction['target']}, {qObjAction['rate']}"
                    )
                for qObjAction in qObj.e:
                    self.edit_boxes[qObj]["e_actions"].addItem(
                        f"{qObjAction['name']}, {qObjAction['target']}, {qObjAction['rate']}"
                    )
                for qObjAction in qObj.q:
                    self.edit_boxes[qObj]["q_actions"].addItem(
                        f"{qObjAction['name']}, {qObjAction['target']}, {qObjAction['rate']}"
                    )
                for qObjAction in qObj.a:
                    self.edit_boxes[qObj]["a_actions"].addItem(
                        f"{qObjAction['name']}, {qObjAction['target']}, {qObjAction['rate']}"
                    )

    def update_queue_display(self):
        """Update the queue display based on the current state of the CombatQueue."""
        self.queue_list.clear()
        queue_state = [
            "{} (行動值: {:.1f})".format(x.name, x.time) for x in self.q.getQueue()
        ]
        for QObj in queue_state:
            self.queue_list.addItem(QObj)