from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QProgressBar,
)
from PyQt6.QtCore import (
    QPropertyAnimation,
    Qt,
    pyqtSignal,
)


class ProjectCard(QFrame):
     
    edit_clicked = pyqtSignal()
    delete_clicked = pyqtSignal()

    def __init__(
        self,
        name,
        deadline,
        priority,
        estimated,
        worked,
        remaining,
        progress,
        status
    ):

        super().__init__()

        self.setObjectName("ProjectCard")

        self.setStyleSheet("""
            QFrame#ProjectCard{
                border:1px solid #008CFF;
                border-radius:8px;
                background:#07131F;
                padding:12px;
            }
            QFrame#ProjectCard:hover{
                background:#0A1B2D;
                border:2px solid #23A6FF;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(6)
        layout.setContentsMargins(10,10,10,10)

        # ---------- Top Row ----------
        header = QFrame()
        header.setFixedHeight(42)

        header.setStyleSheet("""
        QFrame{
            background:#050A12;
            border:none;
            border-bottom:1px solid #123A5A;
        }
        """)

        top_row = QHBoxLayout(header)
        top_row.setContentsMargins(8, 0, 8, 0)
        top_row.setSpacing(8)


        title = QLabel(f"🗁 {name}")
        title.setStyleSheet("""
            font-size:17px;
            font-weight:bold;
            color:white;
            border:none;
        """)

        status_badge = QLabel(status)
        status_badge.setFixedHeight(30)
        status_badge.setFixedSize(82, 26)

        if status == "Completed":

            status_badge.setStyleSheet("""
            QLabel{
                background:#1A321E;
                color:#6CFF9E;
                border:1px solid #42FF90;
                border-radius:5px;
                padding:0px;
                font-size:11px;
                font-weight:bold;
            }
            """)

        else:

            status_badge.setStyleSheet("""
            QLabel{
                background:#0B1E33;
                color:#49C8FF;
                border:1px solid #008CFF;
                border-radius:5px;
                padding:0px;
                font-size:11px;
                font-weight:bold;
            }
            """)

        status_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)


        top_row.addWidget(title)
        top_row.addStretch()
        top_row.addWidget(status_badge)

        layout.addWidget(header)

        info = QLabel(
            f"""
🗓 Deadline : {deadline}

⚡︎ Priority : {priority}

⏱ Estimated : {estimated} h

⏲ Worked : {worked} h

⏱ Remaining : {remaining} h

🗠 Progress : {progress}%
"""
        )

        info.setStyleSheet("""
            border:none;
            font-size:14px;
        """)

        layout.addWidget(info)

        progress_bar = QProgressBar()

        progress_bar.setRange(0,100)
        progress_bar.setValue(progress)

        progress_bar.setTextVisible(True)

        progress_bar.setStyleSheet("""
        QProgressBar{
            border:1px solid #008CFF;
            border-radius:5px;
            background:#06111C;
            height:14px;
        }

        QProgressBar::chunk{
            background:#1EA7FF;
            border-radius:4px;
        }
        """)

        layout.addWidget(progress_bar)

        button_layout = QHBoxLayout()

        self.edit_btn = QPushButton("Edit")
        self.edit_btn.setStyleSheet("""
        QPushButton{
            background:#0B1E33;
            border:1px solid #008CFF;
            border-radius:5px;
            padding:5px 10px;
        }

        QPushButton:hover{
            background:#16476A;
        }
        """)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setStyleSheet("""
        QPushButton{
            background:#2A1111;
            border:1px solid #FF5555;
            border-radius:5px;
            padding:5px 10px;
        }

        QPushButton:hover{
            background:#5A1A1A;
        }
        """)

        button_layout.addStretch()

        button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.delete_btn)

        self.edit_btn.clicked.connect(
            self.edit_clicked.emit
        )


        self.delete_btn.clicked.connect(
            self.delete_clicked.emit
        )

        layout.addLayout(button_layout)

        self.setLayout(layout)