import database.routine_db as routine_db

from dialogs.add_routine_dialog import AddRoutineDialog

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QMenu
)

from PyQt6.QtCore import Qt


class RoutinePage(QWidget):

    def __init__(self, parent=None):

        super().__init__()

        self.main_window = parent

        layout = QVBoxLayout()

        # ================= Toolbar =================

        toolbar = QHBoxLayout()

        title = QLabel("Routine Manager")

        title.setStyleSheet("""
        font-size:26px;
        font-weight:bold;
        """)

        self.add_btn = QPushButton("+ New Routine")

        toolbar.addWidget(title)
        toolbar.addStretch()
        toolbar.addWidget(self.add_btn)

        layout.addLayout(toolbar)

        # ================= List =================

        self.routine_list = QListWidget()

        layout.addWidget(self.routine_list)

        self.setLayout(layout)

        self.add_btn.clicked.connect(
            self.add_routine
        )

        self.routine_list.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )

        self.routine_list.customContextMenuRequested.connect(
            self.context_menu
        )

        self.load_routines()


    def load_routines(self):

        self.routine_list.clear()

        routines = routine_db.get_all_routines()

        days = [
            "Sun",
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat"            
        ]

        for routine in routines:

            (
                rid,
                title,
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

            flags = [
                sun,
                mon,
                tue,
                wed,
                thu,
                fri,
                sat,
            ]

            repeat = ", ".join(
                days[i]
                for i, value in enumerate(flags)
                if value
            )

            status = "✓" if enabled else "✗"

            text = (
                f"{status}  "
                f"{start} - {end}    "
                f"{title}\n"
                f"{repeat}"
            )

            item = QListWidgetItem(text)

            item.setData(
                Qt.ItemDataRole.UserRole,
                rid
            )

            self.routine_list.addItem(item)

    def add_routine(self):

        dialog = AddRoutineDialog()

        if dialog.exec():

            if dialog.start_input.time() >= dialog.end_input.time():
                return

            routine_db.add_routine(

                dialog.title_input.text(),

                dialog.start_input.time().toString("HH:mm"),

                dialog.end_input.time().toString("HH:mm"),

                dialog.sun.isChecked(),

                dialog.mon.isChecked(),

                dialog.tue.isChecked(),

                dialog.wed.isChecked(),

                dialog.thu.isChecked(),

                dialog.fri.isChecked(),

                dialog.sat.isChecked(),

                dialog.enabled.isChecked()

            )

            self.load_routines()

    def context_menu(self, position):

        item = self.routine_list.itemAt(position)

        if not item:
            return

        menu = QMenu()

        edit_action = menu.addAction("Edit")

        delete_action = menu.addAction("Delete")

        action = menu.exec(
            self.routine_list.mapToGlobal(position)
        )

        if action == delete_action:

            routine_db.delete_routine(
                item.data(Qt.ItemDataRole.UserRole)
            )

            self.load_routines()

        elif action == edit_action:

            self.edit_routine(item)

    def edit_routine(self, item):

        routine_id = item.data(Qt.ItemDataRole.UserRole)

        routine = routine_db.get_routine(routine_id)

        if not routine:
            return

        dialog = AddRoutineDialog(routine)

        if dialog.exec():

            if dialog.start_input.time() >= dialog.end_input.time():
                return

            routine_db.update_routine(

                routine_id,

                dialog.title_input.text(),

                dialog.start_input.time().toString("HH:mm"),

                dialog.end_input.time().toString("HH:mm"),

                dialog.sun.isChecked(),

                dialog.mon.isChecked(),

                dialog.tue.isChecked(),

                dialog.wed.isChecked(),

                dialog.thu.isChecked(),

                dialog.fri.isChecked(),

                dialog.sat.isChecked(),

                dialog.enabled.isChecked()

            )

            self.load_routines()
        