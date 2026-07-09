from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)

from PyQt6.QtCore import (
    Qt,
    QDateTime,
    QTimer,
)

class DashboardPage(QWidget):

    def __init__(self, parent=None):
        super().__init__()

        self.main_window = parent

        layout = QVBoxLayout()

        # ================= Header =================

        title = QLabel("Dashboard")
        title.setStyleSheet("""
            font-size: 12px;
            font-weight: bold;
            color: #1EA7FF;
        """)
        subtitle = QLabel("SYRA Command Center")
        self.greeting = QLabel("Hello, Boss..")
        self.date_label = QLabel()
        self.time_label = QLabel()
        self.system_label = QLabel("User: V. Aryan Kabir | System Status: Idle")

        subtitle.setStyleSheet("""
            font-size: 15px;
            color: #9FCFFF;
        """)
        self.greeting.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
            color:#9FCFFF;
        """)

        self.date_label.setStyleSheet("""
            color:#74B8FF;
            font-size:14px;
        """)

        self.time_label.setStyleSheet("""
            color:#1EA7FF;
            font-size:16px;
            font-weight:bold;
        """)

        self.system_label.setStyleSheet("""
            color:#74B8FF;
            font-size:13px;
        """)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addWidget(self.greeting)
        layout.addWidget(self.date_label)
        layout.addWidget(self.time_label)
        layout.addWidget(self.system_label)

        layout.addSpacing(25)

        # ================= Placeholder =================

        placeholder = QLabel(
            """
Today's Tasks

(Coming Soon)


Active Projects

(Coming Soon)


Upcoming Deadlines

(Coming Soon)


AI Status

Idle
"""
        )

        placeholder.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )

        placeholder.setStyleSheet("""
            border:1px solid #008CFF;
            border-radius:8px;
            padding:20px;
            background:#07131F;
            font-size:15px;
        """)

        layout.addWidget(placeholder)

        layout.addStretch()

        self.setLayout(layout)
        self.update_header()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_header)
        self.timer.start(1000)  # Update every second
    
    def update_header(self):

        now = QDateTime.currentDateTime()

        hour = now.time().hour()

        if hour >= 6 and hour < 12:
            greeting = "Good Morning"
        elif hour >= 12 and hour < 18:
            greeting = "Good Afternoon"
        elif hour >= 18 and hour < 24:
            greeting = "Good Evening"

        else:
            greeting = "It's a Great Night"

        self.greeting.setText(f"{greeting}, Boss..")

        self.date_label.setText(
            now.toString("dddd, dd MMMM yyyy")
        )

        self.time_label.setText(
            now.toString("hh:mm AP")
        )