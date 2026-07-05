from PyQt6.QtWidgets import (
    QFormLayout,
    QLineEdit,
    QDateEdit,
    QDialogButtonBox,
    QDialog,
    QSpinBox,
    QComboBox,
)
from PyQt6.QtCore import (
    QDate,
)
# Add Project Dialog Section

class AddProjectDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Project")
        self.resize(450, 300)

        layout = QFormLayout()

        self.name_input = QLineEdit()

        self.deadline_input = QDateEdit()
        self.deadline_input.setDate(QDate.currentDate())
        self.deadline_input.setCalendarPopup(True)
        self.deadline_input.setDisplayFormat("dd-MM-yyyy")

        self.hours_input = QSpinBox()
        self.hours_input.setMaximum(10000)

        self.priority_input = QComboBox()
        self.priority_input.addItems([
            "Low",
            "Medium",
            "High"
        ])

        layout.addRow("Project Name", self.name_input)
        layout.addRow("Deadline", self.deadline_input)
        layout.addRow("Hours Required", self.hours_input)
        layout.addRow("Priority", self.priority_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

        self.setLayout(layout)
