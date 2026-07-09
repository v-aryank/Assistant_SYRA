import sys
from database.database import (
    create_tables,
)
import database.task_db as task_db
from pages.schedule import SchedulePage

from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
)
from PyQt6.QtCore import (
    Qt,
    QSize,
)
from PyQt6.QtGui import QMovie
from dialogs.add_task_dialog import AddTaskDialog
from dialogs.add_project_dialog import AddProjectDialog
import database.project_db as project_db
from pages.projects import ProjectsPage
from pages.dashboard import DashboardPage
from services.project_scheduler import generate_project_recommendation


# SYRA Schedule Main Window SEction
class SYRASchedule(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SYRA - Assistant")
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

        title = QLabel("SYRA")
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
        btn_settings = QPushButton("Settings")

        sidebar.addSpacing(20)
        sidebar.addWidget(btn_dashboard)
        sidebar.addWidget(btn_schedule)
        sidebar.addWidget(btn_routine)
        sidebar.addWidget(btn_projects)
       
        btn_schedule.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.schedule_page)
        )

        btn_projects.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.projects_page)
        )
        
        btn_dashboard.clicked.connect(
            lambda: self.pages.setCurrentWidget(
                self.dashboard_page
            )
        )
        sidebar.addStretch()
        sidebar.addWidget(btn_settings)

        # Sidebar container
        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar)
        sidebar_widget.setFixedWidth(250)

        # ================= Main Area =================
        content = QVBoxLayout()

        

        self.pages = QStackedWidget()

        self.schedule_page = SchedulePage(self)
        self.projects_page = ProjectsPage(self)
        self.dashboard_page = DashboardPage(self)
        self.pages.addWidget(self.schedule_page)
        self.pages.addWidget(self.projects_page)
        self.pages.addWidget(self.dashboard_page)

        content.addWidget(self.pages)
        self.pages.setCurrentWidget(
            self.dashboard_page
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

        self.project_status = QLabel(
        """
        PROJECTS

        0 Active
        """
        )

        self.project_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.project_status.setMinimumHeight(120)
        self.project_status.setStyleSheet(widget_style)

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
        bottom_layout.addWidget(self.project_status)
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

        # Load bottom panel information
        self.refresh_status_panels()

        # Bottom status bar
        status = self.statusBar()
        status.showMessage(
        "SYRA CORE | Voice: Offline | AI: Idle | Schedule Engine: Ready"
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
        QListWidget::item:selected {
            background: rgba(0,140,255,25);
            border: 1px solid #008CFF;
            border-left: 4px solid #1EA7FF;
        }

        QListWidget::item:hover {
            background: rgba(30,167,255,20);
        }
                           
        QLabel {
            color: #D6ECFF;
        }
        """)

    def open_add_project(self):

        dialog = AddProjectDialog()

        if dialog.exec() == QDialog.DialogCode.Accepted:

            project_db.add_project(
                dialog.name_input.text(),
                dialog.deadline_input.date().toString("yyyy-MM-dd"),
                dialog.hours_input.value(),
                dialog.priority_input.currentText()
            )

            print("Project saved successfully.")

            self.refresh_status_panels()
            self.projects_page.load_projects()

    def refresh_status_panels(self):

        count = project_db.get_active_project_count()

        self.project_status.setText(
            f"""
        PROJECTS

        {count} Active
        """
        )
    
    def open_add_task(self):
        dialog = AddTaskDialog()

        if dialog.exec() == QDialog.DialogCode.Accepted:
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

            task_db.add_task(
                title,
                date,
                start_time,
                end_time
            )

            print("Task saved successfully.")
            self.schedule_page.load_tasks()
            self.refresh_status_panels()
           

create_tables()

app = QApplication(sys.argv)

window = SYRASchedule()


window.show()

sys.exit(app.exec())