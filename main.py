import sys
import sqlite3
from tkinter import dialog
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QDateEdit,
    QListWidgetItem,
    QTimeEdit,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QComboBox,
    QDialogButtonBox,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QMenu 
)
from PyQt6.QtCore import (
    Qt,
    QSize,
    QDate,
    QTime
)
from PyQt6.QtGui import QMovie

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

# Edit Task Dialog Section
class EditTaskDialog(AddTaskDialog):

    def __init__(
        self,
        title,
        date,
        start,
        end
    ):
        super().__init__()

        self.setWindowTitle(
            "Edit Task"
        )

        self.title_input.setText(
            title
        )


# SIRA Schedule Main Window SEction
class SIRASchedule(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SIRA Schedule Assistant")
        self.setGeometry(100, 100, 1400, 800)

        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Main layout
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # ================= Sidebar =================
        sidebar = QVBoxLayout()

        logo_container = QVBoxLayout()

        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        movie = QMovie("assets/brain.gif")
        movie.setScaledSize(QSize(140,80))

        logo_label.setMovie(movie)
        movie.start()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("""
            font-size: 42px;
            color: #1EA7FF;
        """)

        title = QLabel("SIRA")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 30px;
            color: #1EA7FF;
            font-weight: bold;
            letter-spacing: 3px;
        """)

        subtitle = QLabel("SYSTEM ACTIVATED")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 11px;
            color: #74B8FF;
            letter-spacing: 2px;
        """)

        logo_container.addWidget(logo_label)
        logo_container.addWidget(title)
        logo_container.addWidget(subtitle)

        sidebar.addLayout(logo_container)

        btn_dashboard = QPushButton("Dashboard")
        btn_schedule = QPushButton("Schedule")
        btn_projects = QPushButton("Projects")
        btn_routine = QPushButton("Routine")
        btn_add_project = QPushButton("+ Add Project")
        btn_add_task = QPushButton("+ Add Task")
        btn_settings = QPushButton("Settings")

        sidebar.addSpacing(20)
        sidebar.addWidget(btn_dashboard)
        sidebar.addWidget(btn_schedule)
        sidebar.addWidget(btn_routine)
        sidebar.addWidget(btn_projects)
        sidebar.addWidget(btn_add_project)
        btn_add_project.clicked.connect(
        self.open_add_project
        )
        sidebar.addWidget(btn_add_task)
        btn_add_task.clicked.connect(
        self.open_add_task
        )
        
        sidebar.addStretch()
        sidebar.addWidget(btn_settings)

        # Sidebar container
        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar)
        sidebar_widget.setFixedWidth(250)

        # ================= Main Area =================
        content = QVBoxLayout()

        # ---------- Schedule Header ----------

        toolbar = QHBoxLayout()

        self.schedule_title = QLabel("Today's Schedule")
        self.schedule_title.setStyleSheet("""
        font-size: 26px;
        color: #1EA7FF;
        font-weight: bold;
        """)
        self.view_selector = QComboBox()
        self.view_selector.addItems([
            "Today",
            "Tomorrow",
            "This Week",
            "All Tasks"
        ])
        toolbar = QHBoxLayout()
        toolbar.addWidget(self.schedule_title)
        toolbar.addStretch()
        toolbar.addWidget(self.view_selector)

        content.addLayout(toolbar)
        self.task_list = QListWidget()
        content.addWidget(self.task_list)

        #Load tasks after creating the dropdwn
        self.load_tasks()
        
        #Refresh tasks when the dropdown selection changes
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

        # ====================================================
        # Bottom Information Panels
        # ====================================================

        bottom_layout = QHBoxLayout()

        widget_style = """
        background-color: #07131F;
        border: 1px solid #008CFF;
        border-radius: 6px;
        padding: 15px;
        font-size: 14px;
        color: #D6ECFF;
        """

        # ---------------- AI STATUS ----------------

        ai_status = QLabel(
        """
        AI STATUS

        Idle
        """
        )

        ai_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ai_status.setMinimumHeight(120)
        ai_status.setStyleSheet(widget_style)

        # ---------------- PROJECTS ----------------

        project_status = QLabel(
        """
        PROJECTS

        0 Active
        """
        )

        project_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        project_status.setMinimumHeight(120)
        project_status.setStyleSheet(widget_style)

        # ---------------- FOCUS MODE ----------------

        focus_status = QLabel(
        """
        FOCUS MODE

        Disabled
        """
        )

        focus_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        focus_status.setMinimumHeight(120)
        focus_status.setStyleSheet(widget_style)

        # Add widgets to horizontal layout

        bottom_layout.addWidget(ai_status)
        bottom_layout.addWidget(project_status)
        bottom_layout.addWidget(focus_status)

        # Add bottom layout to main content

        content.addSpacing(15)
        content.addLayout(bottom_layout)

        # Create content widget

        content_widget = QWidget()
        content_widget.setLayout(content)

        # Add to main layout
        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(content_widget)

        # Bottom status bar
        status = self.statusBar()
        status.showMessage(
        "SIRA CORE | Voice: Offline | AI: Idle | Schedule Engine: Ready"
        )   

        # Global style
        self.setStyleSheet("""
        QMainWindow {
            background-color: #05080F;
        }

        QWidget {
            background-color: #05080F;
            color: #D6ECFF;
            font-family: "Terminus (TTF)";
        }

        QPushButton {
            background-color: #07131F;
            border: 1px solid #008CFF;
            border-radius: 6px;
            padding: 12px;
            color: #D6ECFF;
            font-size: 14px;
        }

        QPushButton:hover {
            background-color: #0B1E33;
            border: 1px solid #1EA7FF;
        }

        QListWidget {
            background-color: #07131F;
            border: 1px solid #008CFF;
            border-radius: 6px;
            padding: 10px;
            color: #D6ECFF;
        }

        QLabel {
            color: #D6ECFF;
        }
        """)

    def open_add_project(self):
        dialog = AddProjectDialog()

        if dialog.exec():
            print(
                dialog.name_input.text(),
                dialog.deadline_input.text(),
                dialog.hours_input.value(),
                dialog.priority_input.currentText()
            )
    
    def open_add_task(self):
        dialog = AddTaskDialog()

        if dialog.exec():

         title = dialog.title_input.text()

        date = dialog.date_input.date().toString(
            "yyyy-MM-dd"
        )

        start_time = dialog.start_input.time().toString(
            "HH:mm"
        )

        end_time = dialog.end_input.time().toString(
            "HH:mm"
        )

        conn = sqlite3.connect("sira_schedule.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO tasks
        (title, date, start_time, end_time)
        VALUES (?, ?, ?, ?)
        """, (
            title,
            date,
            start_time,
            end_time
        ))

        conn.commit()
        conn.close()

        print("Task saved successfully.")
        self.load_tasks()

    def load_tasks(self):

        self.task_list.clear()

        conn = sqlite3.connect("sira_schedule.db")
        cursor = conn.cursor()

        selected = self.view_selector.currentText()

        # ================= TODAY =================

        if selected == "Today":

            today = QDate.currentDate().toString("yyyy-MM-dd")
            
            self.schedule_title.setText("Today's Schedule")
            cursor.execute("""
                SELECT id, title, date, start_time, end_time, completed
                FROM tasks
                WHERE date = ?
                ORDER BY start_time
            """, (today,))

        # ================= TOMORROW =================

        elif selected == "Tomorrow":

            tomorrow = QDate.currentDate().addDays(1).toString("yyyy-MM-dd")

            self.schedule_title.setText("Tomorrow's Schedule")
            cursor.execute("""
                SELECT id, title, date, start_time, end_time, completed
                FROM tasks
                WHERE date = ?
                ORDER BY start_time
            """, (tomorrow,))

        # ================= THIS WEEK =================

        elif selected == "This Week":

            today = QDate.currentDate().toString("yyyy-MM-dd")
            end_week = QDate.currentDate().addDays(6).toString("yyyy-MM-dd")

            self.schedule_title.setText("This Week's Schedule")
            cursor.execute("""
                SELECT id, title, date, start_time, end_time, completed
                FROM tasks
                WHERE date BETWEEN ? AND ?
                ORDER BY date, start_time
            """, (today, end_week))

        # ================= ALL TASKS =================

        else:
            self.schedule_title.setText("All Tasks")
            cursor.execute("""
                SELECT id, title, date, start_time, end_time, completed
                FROM tasks
                ORDER BY date, start_time
            """)

        tasks = cursor.fetchall()

        conn.close()

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

        task_id = item.data(
            Qt.ItemDataRole.UserRole
        )

        conn = sqlite3.connect(
            "sira_schedule.db"
        )

        cursor = conn.cursor()

        cursor.execute("""
            SELECT completed
            FROM tasks
            WHERE id = ?
        """, (task_id,))

        current = cursor.fetchone()[0]

        new_value = 0 if current else 1

        cursor.execute("""
            UPDATE tasks
            SET completed = ?
            WHERE id = ?
        """, (
            new_value,
            task_id
        ))

        conn.commit()
        conn.close()

        self.load_tasks()

    def edit_task(self, item):

        task_id = item.data(
            Qt.ItemDataRole.UserRole
        )

        conn = sqlite3.connect(
            "sira_schedule.db"
        )

        cursor = conn.cursor()

        cursor.execute("""
            SELECT title, date, start_time, end_time
            FROM tasks
            WHERE id = ?
        """, (task_id,))

        task_data = cursor.fetchone()
        conn.close()

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

                conn = sqlite3.connect(
                    "sira_schedule.db"
                )
                cursor = conn.cursor()

                cursor.execute("""
                    UPDATE tasks
                    SET title = ?, date = ?, start_time = ?, end_time = ?
                    WHERE id = ?
                """, (
                    new_title,
                    new_date,
                    new_start_time,
                    new_end_time,
                    task_id
                ))

                conn.commit()
                conn.close()

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

            conn = sqlite3.connect(
                "sira_schedule.db"
            )

            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM tasks
                WHERE id = ?
            """, (task_id,))

            conn.commit()
            conn.close()

            self.load_tasks()
        
        elif action == edit_action:
            self.edit_task(item)







app = QApplication(sys.argv)

window = SIRASchedule()
window.show()

sys.exit(app.exec())