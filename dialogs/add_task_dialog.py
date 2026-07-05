
from PyQt6.QtWidgets import (
    QFormLayout,
    QLineEdit,
    QDateEdit,
    QTimeEdit,
    QDialogButtonBox,
    QDialog,
)
from PyQt6.QtCore import (
    QDate,
    QTime
)

# Add Task Dialog Section
class AddTaskDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Task")
        self.resize(450, 300)

        layout = QFormLayout()

        self.title_input = QLineEdit()

        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("dd-MM-yyyy")

        self.start_input = QTimeEdit()
        self.start_input.setTime(QTime.currentTime())

        self.end_input = QTimeEdit()
        self.end_input.setTime(QTime.currentTime())

        layout.addRow("Task Name", self.title_input)
        layout.addRow("Date", self.date_input)
        layout.addRow("Start Time", self.start_input)
        layout.addRow("End Time", self.end_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

        self.setLayout(layout)