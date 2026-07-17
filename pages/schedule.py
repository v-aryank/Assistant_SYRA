import database.task_db as task_db
import database.project_db as project_db
import database.routine_db as routine_db

from dialogs.edit_task_dialog import EditTaskDialog
from services.project_scheduler import (
    generate_daily_schedule
)
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
        content_layout = QVBoxLayout()

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
        

        # ---------- Main Content ----------

        content_layout = QHBoxLayout()

        # ================= LEFT =================

        left_panel = QVBoxLayout()

        self.task_list = QListWidget()

        left_panel.addWidget(
            self.task_list,
            7
        )

        # ================= RIGHT =================

        right_panel = QVBoxLayout()

        right_title = QLabel("Statistics")
        right_title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #1EA7FF;
            padding-bottom: 8px; 
             """)
        right_panel.addWidget(right_title)
        self.total_label = QLabel("Total Tasks : 0")
        self.completed_label = QLabel("Completed : 0")
        self.remaining_label = QLabel("Remaining : 0")
        self.percent_label = QLabel("Completion : 0%")

        # ---------- Next Task ----------
        self.next_task_label = QLabel(
            "🗒 Next Task\n\nNo upcoming task"
        )

        # ---------- Upcoming Deadline ----------
        self.deadline_label = QLabel(
            "🗓 Upcoming Deadline\n\nNo active project"
        )

        # ---------- AI Insight ----------
        self.ai_label = QLabel(
            ".✦ ݁˖ AI Insight\n\nSystem analysing..."
        )
        

        for label in (
            self.total_label,
            self.completed_label,
            self.remaining_label,
            self.percent_label,
            self.next_task_label,
            self.deadline_label,
            self.ai_label
        ):
            label.setStyleSheet("""
                border:1px solid #008CFF;
                border-radius:8px;
                padding:8px;
                background:#07131F;
                font-size:15px;
            """)

        right_panel.addWidget(self.total_label)
        right_panel.addWidget(self.completed_label)
        right_panel.addWidget(self.remaining_label)
        right_panel.addWidget(self.percent_label)
            
        right_panel.addSpacing(15)

        right_panel.addWidget(self.next_task_label)

        right_panel.addWidget(self.deadline_label)

        right_panel.addWidget(self.ai_label)

        right_panel.addStretch()

        content_layout.addLayout(
 
           left_panel,
            7
        )
        content_layout.addLayout(
            right_panel,
            3
        )

        layout.addLayout(content_layout)

        # =====================================================
        # SYRA Recommendation Panel
        # =====================================================

        self.recommend_box = QWidget()

        recommend_layout = QVBoxLayout()

        title = QLabel(".✦ ݁ 🕮 SYRA Recommendation.✦ ݁ ݁")

        title.setStyleSheet("""
        font-size:20px;
        font-weight:bold;
        color:#1EA7FF;
        """)

        self.recommend_text = QLabel(
        """
        No recommendation available.
        """
        )

        self.recommend_text.setStyleSheet("""
        border:1px solid #008CFF;
        border-radius:8px;
        padding:8px;
        background:#07131F;
        font-size:14px;
        """)

        buttons = QHBoxLayout()

        self.accept_btn = QPushButton("Accept")
        self.accept_btn.clicked.connect(
            self.accept_recommendation
        )

        self.reject_btn = QPushButton("Reject")
        self.reject_btn.clicked.connect(
            self.reject_recommendation
        )

        buttons.addStretch()
        buttons.addWidget(self.accept_btn)
        buttons.addWidget(self.reject_btn)

        recommend_layout.addWidget(title)
        recommend_layout.addWidget(self.recommend_text)
        recommend_layout.addLayout(buttons)

        self.recommend_box.setLayout(
            recommend_layout
        )

        layout.addSpacing(15)

        left_panel.addWidget(
            self.recommend_box,
            3
        )



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
        self.refresh_statistics()
    
    def refresh_statistics(self):

        total = self.task_list.count()

        completed = 0

        for i in range(total):

            item = self.task_list.item(i)

            if item.text().startswith("☑"):
                completed += 1

        remaining = total - completed

        percent = 0

        if total > 0:
            percent = int((completed / total) * 100)

        self.total_label.setText(
            f"Total Tasks : {total}"
        )

        self.completed_label.setText(
            f"Completed : {completed}"
        )

        self.remaining_label.setText(
            f"Remaining : {remaining}"
        )

        self.percent_label.setText(
            f"Completion : {percent}%"
        )
        
        # ----------- Next Task ----------
        today = QDate.currentDate().toString("yyyy-MM-dd")

        task = task_db.get_next_task(
            today,
            QTime.currentTime().toString("HH:mm"))

        if task:

            title, start, end = task

            self.next_task_label.setText(
                f"""
        🗒 Next Task

        {title}

        {start} - {end}
        """
            )

        else:

            self.next_task_label.setText(
                """
        🗒 Next Task

        No upcoming task
        """
            )
        
        # ----------- Upcoming Deadline ----------
        project = project_db.get_next_deadline()

        if project:

            name, deadline = project

            deadline_date = QDate.fromString(
                deadline,
                "yyyy-MM-dd"
            )

            days = QDate.currentDate().daysTo(deadline_date)

            if days == 0:
                deadline_text = "Today"

            elif days == 1:
                deadline_text = "Tomorrow"

            else:
                deadline_text = f"{days} days remaining"

            self.deadline_label.setText(
                f"""
        🗓 Upcoming Deadline

        {name}

        {deadline_date.toString("dd MMM yyyy")}

        {deadline_text}
        """
            )

        else:

            self.deadline_label.setText(
                """
        🗓 Upcoming Deadline

        No active project
        """
            )
        
        # ---------- AI Insight ----------
        self.update_ai_insight(
            total,
            completed,
            remaining
        )

        recommendations = generate_daily_schedule()

        if recommendations:
            self.update_recommendation(
                recommendations[0]
            )
        else:
            self.update_recommendation(None)

    def update_ai_insight(
        self,
        total,
        completed,
        remaining
    ):

        if total == 0:

            text = (
                "No tasks scheduled today.\n"
                "A good day to plan ahead."
            )

        elif completed == total:

            text = (
                "Excellent work.\n"
                "Today's schedule is complete."
            )

        elif completed == 0:

            text = (
                "Start with your first task.\n"
                "Momentum matters."
            )

        elif remaining >= 5:

            text = (
                "Busy day ahead.\n"
                "Focus on one task at a time."
            )

        else:

            text = (
                "You're making progress.\n"
                "Keep going."
            )

        self.ai_label.setText(
            f"""
        .✦ ݁˖ AI Insight

        {text}
        """
            )
    
    def format_duration(self, hours):

        total_minutes = round(hours * 60)

        h = total_minutes // 60
        m = total_minutes % 60

        if h > 0 and m > 0:
            return f"{h} h {m} min"

        elif h > 0:
            return f"{h} h"

        else:
            return f"{m} min"
        
    def update_recommendation(self, recommendation):

        self.current_recommendation = recommendation

        if recommendation is None:

            self.recommend_text.setText(
                "No recommendation available today."
            )

            return

        slot = recommendation["recommended_slot"]

        project = recommendation["name"]

        target = self.format_duration(
            recommendation["target_minutes"] / 60
        )

        scheduled = self.format_duration(
            recommendation["scheduled_minutes"] / 60
        )

        remaining = self.format_duration(
            recommendation["remaining_minutes"] / 60
        )

        if slot:

            start = slot["scheduled_start"]
            end = slot["scheduled_end"]


            if slot["completed"]:

                status = "Your full target can be completed today."

            else:

                status = (
                    "Only part of today's target fits into your schedule."
                )


            message = (
                f"Sir, you have a free time slot between "
                f"{start} - {end}.\n\n"

                f"I recommend working on:\n"

                f"Project : {project}\n"
                f"Today's Target : {target}\n"
                f"Available Slot : {scheduled}\n"
                f"Remaining Today : {remaining}\n\n"

                f"{status}\n\n"

                f"Should I schedule it?"
            )

        else:

            message = (
                f"Sir, today's most urgent project is:\n\n"

                f"Project : {project}\n"
                f"Today's Target : {target}\n\n"

                f"I couldn't find any suitable free time slot today.\n"
                f"You may need to reschedule some existing tasks."
            )

        self.recommend_text.setText(message)

    def accept_recommendation(self):

        if not self.current_recommendation:
            return

        slot = self.current_recommendation["recommended_slot"]

        if slot is None:
            return

        task_db.add_project_session(

            self.current_recommendation["project_id"],

            self.current_recommendation["name"],

            QDate.currentDate().toString("yyyy-MM-dd"),

            slot["scheduled_start"],

            slot["scheduled_end"],

            slot["scheduled_minutes"]

        )

        self.main_window.refresh_all()
        
    def reject_recommendation(self):

        self.current_recommendation = None

        self.recommend_text.setText(
            "Recommendation dismissed."
        )


    def toggle_task_completed(self, item):

        task_id = item.data(Qt.ItemDataRole.UserRole)

        completed = task_db.toggle_task_completion(task_id)
        task = task_db.get_project_task(task_id)

        if task:

            project_id, minutes, system = task

            if system and project_id is not None:

                if completed:

                    project_db.add_worked_minutes(
                        project_id,
                        minutes
                    )

                else:

                    project_db.remove_worked_minutes(
                        project_id,
                        minutes
                    )
        
        self.main_window.refresh_all()

    
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

            self.main_window.refresh_all()
        
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

                self.main_window.refresh_all()
 

