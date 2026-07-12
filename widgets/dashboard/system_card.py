from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
)
from PyQt6.QtCore import Qt


class SystemCard(QWidget):
    """
    Reusable HUD-style card widget.
    Usage:
        card = SystemCard("Vital Signs")
        card.add_row("Heart Rate", "72 BPM")
        card.add_row("Body Temp", "98.6 °F")
    """

    def __init__(self, title, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(8)
        self.layout.setContentsMargins(14, 12, 14, 12)

        self.title_label = QLabel(title.upper())
        self.title_label.setStyleSheet("""
            color: #74B8FF;
            font-size: 11px;
            font-weight: bold;
            letter-spacing: 2px;
            border: none;
            background: transparent;
        """)

        self.layout.addWidget(self.title_label)
        self.setLayout(self.layout)

        self.setStyleSheet("""
            SystemCard {
                background-color: #07131F;
                border: 1px solid #008CFF;
                border-radius: 6px;
            }
        """)

    def add_row(self, label_text, value_text=""):
        row = QHBoxLayout()

        label = QLabel(label_text)
        label.setStyleSheet("""
            color: #9FCFFF;
            font-size: 13px;
            border: none;
            background: transparent;
        """)

        value = QLabel(value_text)
        value.setObjectName(f"val_{label_text.replace(' ', '_')}")
        value.setAlignment(Qt.AlignmentFlag.AlignRight)
        value.setStyleSheet("""
            color: #1EA7FF;
            font-size: 14px;
            font-weight: bold;
            border: none;
            background: transparent;
        """)

        row.addWidget(label)
        row.addStretch()
        row.addWidget(value)

        self.layout.addLayout(row)
        return value  # return so caller can update it later via .setText()

    def add_widget(self, widget):
        """Drop in something custom (e.g. a mini bar chart, button row)."""
        self.layout.addWidget(widget)