from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QProgressBar,
)
from PyQt6.QtCore import QPropertyAnimation


class ProjectCard(QFrame):

    def __init__(
        self,
        name,
        deadline,
        priority,
        estimated,
        worked,
        remaining,
        progress
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

        title = QLabel(f"🗁 {name}")
        title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
            color:white;
            border:none;
        """)

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

        layout.addWidget(title)
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

        layout.addLayout(button_layout)

        self.setLayout(layout)