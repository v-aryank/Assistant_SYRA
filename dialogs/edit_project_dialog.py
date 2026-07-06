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
# Edit Project Dialog Section

class EditProjectDialog(QDialog):
    def __init__(
        self,
        name,
        deadline,
        estimated_hours_required,
        priority
    ):
        super().__init__()

        self.setWindowTitle("Edit Project")
        self.resize(450, 300)

        layout = QFormLayout()

        self.name_input = QLineEdit(name)

        self.deadline_input = QDateEdit()
        self.deadline_input.setDate(deadline)
        self.deadline_input.setCalendarPopup(True)
        self.deadline_input.setDisplayFormat("dd-MM-yyyy")

        self.hours_input = QSpinBox()
        self.hours_input.setMaximum(10000)
        self.hours_input.setValue(estimated_hours_required)
        self.priority_input = QComboBox()
        self.priority_input.addItems([
            "Low",
            "Medium",
            "High"
        ])
        self.priority_input.setCurrentText(priority)

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
