from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
)
from PyQt6.QtCore import Qt, QDateTime, QTimer
from utils import theme
from widgets.dashboard.system_card import SystemCard
from widgets.dashboard.core_widget import CoreWidget
from widgets.dashboard.activity_log import ActivityLog
import database.project_db as project_db # adjust import path if this is database.project_db


class DashboardPage(QWidget):

    def __init__(self, parent=None):
        super().__init__()

        self.main_window = parent

        root = QVBoxLayout()
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(15)

        # ================= Header =================

        title = QLabel("DASHBOARD")
        title.setStyleSheet(f"""
            font-size: 13px;
            font-weight: bold;
            letter-spacing: 3px;
            color: {theme.PRIMARY};
            border: none;
        """)

        self.greeting = QLabel("Hello, Boss..")
        self.greeting.setStyleSheet(f"""
            font-size: 24px;
            font-weight: bold;
            color: {theme.TEXT_SECONDARY};
            border: none;
        """)
        subtitle = QLabel("User: V. Aryan Kabir | System: Ready")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(f"""
            color: {theme.TEXT_DIM};
            font-size: 12px;
            border: none;
        """)

        header_row = QHBoxLayout()
        header_left = QVBoxLayout()
        header_left.addWidget(title)
        header_left.addWidget(self.greeting)

        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.time_label.setStyleSheet(f"""
            color: {theme.PRIMARY};
            font-size: 16px;
            font-weight: bold;
            border: none;
        """)
        self.date_label = QLabel()
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.date_label.setStyleSheet(f"""
            color: {theme.TEXT_DIM};
            font-size: 12px;
            border: none;
        """)
        header_right = QVBoxLayout()
        header_right.addWidget(self.time_label)
        header_right.addWidget(self.date_label)

        header_row.addLayout(header_left)
        header_row.addStretch()
        header_row.addLayout(header_right)

        root.addLayout(header_row)
        root.addSpacing(10)

        # ================= Main HUD Grid =================

        grid = QGridLayout()
        grid.setSpacing(15)

        # ---- Left column ----
        left_col = QVBoxLayout()
        left_col.setSpacing(15)

        self.vitals_card = SystemCard("System Vitals")
        self.vitals_val_status = self.vitals_card.add_row("AI Status", "Idle")
        self.vitals_val_voice = self.vitals_card.add_row("Voice Link", "Offline")

        self.resources_card = SystemCard("System Resources")
        self.resources_val_tasks = self.resources_card.add_row("Today's Tasks", "0")
        self.resources_val_focus = self.resources_card.add_row("Focus Mode", "Disabled")

        left_col.addWidget(self.vitals_card)
        left_col.addWidget(self.resources_card)

        left_widget = QWidget()
        left_widget.setLayout(left_col)

        # ---- Center column ----
        center_col = QVBoxLayout()
        center_col.setSpacing(10)

        self.core_widget = CoreWidget()

        self.core_caption = QLabel("● ONLINE")
        self.core_caption.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.core_caption.setStyleSheet(f"""
            color: {theme.PRIMARY};
            font-size: 13px;
            letter-spacing: 3px;
            font-weight: bold;
            border: none;
        """)


        center_col.addWidget(self.core_widget)
        center_col.addWidget(self.core_caption)

        center_widget = QWidget()
        center_widget.setLayout(center_col)

        # ---- Right column ----
        right_col = QVBoxLayout()
        right_col.setSpacing(15)

        self.projects_card = SystemCard("Projects")
        self.projects_val_active = self.projects_card.add_row("Active", "0")
        self.projects_val_deadline = self.projects_card.add_row("Next Deadline", "—")

        self.activity_log = ActivityLog()

        right_col.addWidget(self.projects_card)
        right_col.addWidget(self.activity_log)

        right_widget = QWidget()
        right_widget.setLayout(right_col)

        # ---- Assemble grid: left | center | right ----
        grid.addWidget(left_widget, 0, 0)
        grid.addWidget(center_widget, 0, 1)
        grid.addWidget(right_widget, 0, 2)

        grid.setColumnStretch(0, 2)
        grid.setColumnStretch(1, 3)
        grid.setColumnStretch(2, 2)

        root.addLayout(grid)
        root.addStretch()

        self.setLayout(root)

        # ================= Timers =================

        self.update_header()
        self.refresh_data()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_header)
        self.timer.start(1000)

    def update_header(self):
        now = QDateTime.currentDateTime()
        hour = now.time().hour()

        if 6 <= hour < 12:
            greeting = "Good Morning"
        elif 12 <= hour < 18:
            greeting = "Good Afternoon"
        elif 18 <= hour < 24:
            greeting = "Good Evening"
        else:
            greeting = "It's a Great Night"

        self.greeting.setText(f"{greeting}, Boss..")
        self.date_label.setText(now.toString("dddd, dd MMMM yyyy"))
        self.time_label.setText(now.toString("hh:mm AP"))

    def refresh_data(self):
        """Pull live counts from the DB into the cards."""
        try:
            count = project_db.get_active_project_count()
            self.projects_val_active.setText(str(count))
        except Exception as e:
            self.activity_log.log(f"Failed to load project count: {e}")

    def log_event(self, message):
        """Expose a hook so main.py can push events into the terminal panel."""
        self.activity_log.log(message)