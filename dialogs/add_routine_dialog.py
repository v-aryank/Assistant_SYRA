from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QTimeEdit,
    QCheckBox,
    QComboBox
)

from PyQt6.QtCore import QTime

class AddRoutineDialog(QDialog):

    def __init__(self, routine=None):
        super().__init__()

        self.setWindowTitle("Add Routine")
        self.resize(420, 430)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Routine Title"))

        self.title_input = QLineEdit()

        layout.addWidget(self.title_input)

        self.category_input = QComboBox()

        self.category_input.addItems([
            "Personal",
            "University",
            "Study",
            "Meal",
            "Health",
            "Prayer",
            "Travel",
            "Sleep",
            "Other"
        ])

        layout.addWidget(QLabel("Category"))
        layout.addWidget(self.category_input)

        self.show_in_schedule = QCheckBox(
            "Show in Schedule"
        )

        self.show_in_schedule.setChecked(True)

        layout.addWidget(self.show_in_schedule)
        
        layout.addWidget(QLabel("Start Time"))

        self.start_input = QTimeEdit()

        self.start_input.setTime(QTime(9, 0))

        self.start_input.setDisplayFormat("HH:mm")

        layout.addWidget(self.start_input)


        layout.addWidget(QLabel("End Time"))

        self.end_input = QTimeEdit()

        self.end_input.setTime(QTime(10, 0))

        self.end_input.setDisplayFormat("HH:mm")

        layout.addWidget(self.end_input)

        layout.addWidget(QLabel("Repeat On"))

        self.sun = QCheckBox("Sunday")
        self.mon = QCheckBox("Monday")
        self.tue = QCheckBox("Tuesday")
        self.wed = QCheckBox("Wednesday")
        self.thu = QCheckBox("Thursday")
        self.fri = QCheckBox("Friday")
        self.sat = QCheckBox("Saturday")

        layout.addWidget(self.sun)
        layout.addWidget(self.mon)
        layout.addWidget(self.tue)
        layout.addWidget(self.wed)
        layout.addWidget(self.thu)
        layout.addWidget(self.fri)
        layout.addWidget(self.sat)

        self.enabled = QCheckBox("Enabled")

        self.enabled.setChecked(True)

        layout.addWidget(self.enabled)

        buttons = QHBoxLayout()

        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")

        buttons.addStretch()
        buttons.addWidget(save_btn)
        buttons.addWidget(cancel_btn)

        layout.addLayout(buttons)

        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)


        if routine:

            (
                title,
                category,
                visible,
                start,
                end,
                sun,
                mon,
                tue,
                wed,
                thu,
                fri,
                sat,
                enabled
            ) = routine

            self.title_input.setText(title)

            self.category_input.setCurrentText(category)

            self.show_in_schedule.setChecked(bool(visible))

            self.start_input.setTime(
                QTime.fromString(start, "HH:mm")
            )

            self.end_input.setTime(
                QTime.fromString(end, "HH:mm")
            )

            self.sun.setChecked(bool(sun))
            self.mon.setChecked(bool(mon))
            self.tue.setChecked(bool(tue))
            self.wed.setChecked(bool(wed))
            self.thu.setChecked(bool(thu))
            self.fri.setChecked(bool(fri))
            self.sat.setChecked(bool(sat))

            self.enabled.setChecked(bool(enabled))

        self.setLayout(layout)