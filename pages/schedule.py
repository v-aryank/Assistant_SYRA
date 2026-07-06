import database.task_db as task_db
from dialogs.edit_task_dialog import EditTaskDialog
from PyQt6.QtWidgets import (
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QDialog,
)

from PyQt6.QtCore import (
    Qt, 
    QDate, 
    QTime
)

class SchedulePage(QWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.main_window = parent

        layout = QVBoxLayout()

        # ---------- Toolbar ----------

        toolbar = QHBoxLayout()

        self.schedule_title = QLabel("Today's Schedule")
        self.schedule_title.setStyleSheet("font-size: 26px; font-weight: bold;")
        
        
        self.new_task_btn = QPushButton("+ New Task")
        self.view_selector = QComboBox()
        self.view_selector.addItems([
            "Today",
            "Tomorrow",
            "This Week",
            "All Tasks"
        ])

        toolbar.addWidget(self.schedule_title)
        toolbar.addStretch()
        toolbar.addWidget(self.new_task_btn)
        toolbar.addWidget(self.view_selector)

        layout.addLayout(toolbar)

        # ---------- Task List ----------

        self.task_list = QListWidget()

        layout.addWidget(self.task_list)

        self.setLayout(layout)

    # ---------- Refresh tasks when the dropdown selection changes ----------
        self.view_selector.currentIndexChanged.connect(
            self.load_tasks
        )

    # ---------- Schedule List ----------

        self.task_list.itemClicked.connect(
            self.toggle_task_completed
        )
        
        self.task_list.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )

        self.task_list.customContextMenuRequested.connect(
            self.task_context_menu
        )
        self.new_task_btn.clicked.connect(
            self.main_window.open_add_task
        )
    #Load tasks after creating the dropdwn
        self.load_tasks()


    def load_tasks(self):

        self.task_list.clear()

        selected = self.view_selector.currentText()

        # ================= Update Schedule Title =================

        titles = {
            "Today": "Today's Schedule",
            "Tomorrow": "Tomorrow's Schedule",
            "This Week": "This Week's Schedule",
            "All Tasks": "All Tasks"
        }

        self.schedule_title.setText(
            titles.get(selected, "Schedule")
        )

        today = QDate.currentDate().toString("yyyy-MM-dd")
        tomorrow = QDate.currentDate().addDays(1).toString("yyyy-MM-dd")
        end_week = QDate.currentDate().addDays(6).toString("yyyy-MM-dd")

        tasks = task_db.get_tasks(
            selected,
            today,
            tomorrow,
            end_week
        )
        # ================= LOAD TASKS =================

        for task in tasks:

            task_id, title, date, start, end, completed = task

            prefix = "☑" if completed else "☐"

            date_text = QDate.fromString(
                date,
                "yyyy-MM-dd"
            ).toString("ddd dd MMM")

            if selected in ("Today", "Tomorrow"):

                text = (
                    f"{prefix} {start} - {end}   {title}"
                )

            else:

                text = (
                    f"{prefix} {date_text} | {start} - {end} | {title}"
                )


            item = QListWidgetItem(text)

            item.setData(
                Qt.ItemDataRole.UserRole,
                task_id
            )

            self.task_list.addItem(item)


    def toggle_task_completed(self, item):

        task_id = item.data(Qt.ItemDataRole.UserRole)

        task_db.toggle_task_completion(task_id)

        self.load_tasks()

    
    def task_context_menu(self, position):

        item = self.task_list.itemAt(position)

        if not item:
            return

        menu = QMenu()

        delete_action = menu.addAction(
            "Delete Task"
        )
        edit_action = menu.addAction(
            "Edit Task"
        )

        action = menu.exec(
            self.task_list.mapToGlobal(position)
        )

        if action == delete_action:

            task_id = item.data(
                Qt.ItemDataRole.UserRole
            )

            task_db.delete_task(task_id)

            self.load_tasks()
        
        elif action == edit_action:
            self.edit_task(item)


    def edit_task(self, item):

        task_id = item.data(
            Qt.ItemDataRole.UserRole
        )

        task_data = task_db.get_task(task_id)

        if task_data:
            title, date, start_time, end_time = task_data

            dialog = EditTaskDialog(
                title,
                QDate.fromString(date, "yyyy-MM-dd"),
                QTime.fromString(start_time, "HH:mm"),
                QTime.fromString(end_time, "HH:mm")
            )

            if dialog.exec():
                new_title = dialog.title_input.text()
                new_date = dialog.date_input.date().toString("yyyy-MM-dd")
                new_start_time = dialog.start_input.time().toString("HH:mm")
                new_end_time = dialog.end_input.time().toString("HH:mm")

                task_db.update_task(
                    task_id,
                    new_title,
                    new_date,
                    new_start_time,
                    new_end_time
                )

                self.load_tasks()
 

