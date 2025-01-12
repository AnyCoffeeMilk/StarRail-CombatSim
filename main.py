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
    QFormLayout,
)
from PyQt5.QtCore import Qt
from utils.QObject.PlayerQObject import PlayerQObject
from utils.QObject.TurnQObject import TurnQObject
from utils.CombatQueue import CombatQueue


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
        self.setGeometry(100, 100, 800, 600)

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

        self.queue_layout.addWidget(self.queue_label)
        self.queue_layout.addWidget(self.queue_list)

        # Editable fields for each PlayerQObject
        self.objects_form = QFormLayout()
        self.edit_boxes = {}  # To store input fields for each object

        for obj in self.q.getQueue():
            if not isinstance(obj, TurnQObject):
                obj_group = QGroupBox(f"{obj.name}")
                obj_layout = QFormLayout()

                # Name field
                name_input = QLineEdit(obj.name)
                name_input.textChanged.connect(
                    lambda text, o=obj: self.update_name(o, text)
                )
                obj_layout.addRow("名稱:", name_input)

                # Speed field
                speed_input = QLineEdit(str(obj.speed))
                speed_input.textChanged.connect(
                    lambda text, o=obj: self.update_speed(o, text)
                )
                obj_layout.addRow("速度:", speed_input)

                # E Action
                e_target_input = QLineEdit()
                e_percentage_input = QLineEdit()
                e_button = QPushButton("E")
                e_button.clicked.connect(
                    lambda _, o=obj, t=e_target_input, p=e_percentage_input: self.handle_e_action(
                        o, t, p
                    )
                )
                obj_layout.addRow("E Target:", e_target_input)
                obj_layout.addRow("E Percentage:", e_percentage_input)
                obj_layout.addRow(e_button)

                # Q Action
                q_target_input = QLineEdit()
                q_percentage_input = QLineEdit()
                q_button = QPushButton("Q")
                q_button.clicked.connect(
                    lambda _, o=obj, t=q_target_input, p=q_percentage_input: self.handle_q_action(
                        o, t, p
                    )
                )
                obj_layout.addRow("Q Target:", q_target_input)
                obj_layout.addRow("Q Percentage:", q_percentage_input)
                obj_layout.addRow(q_button)

                # A Action
                q_button = QPushButton("A")
                q_button.clicked.connect(lambda _: self.handle_action())
                obj_layout.addRow(q_button)

                obj_group.setLayout(obj_layout)
                self.edit_layout.addWidget(obj_group)
                self.edit_boxes[obj] = {"name": name_input, "speed": speed_input}

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
            if target_input.text() != "":
                target = target_input.text()
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
            if target_input.text() != "":
                target = target_input.text()
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
