from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtCore import QDateTime
from utils import theme


class ActivityLog(QTextEdit):
    """
    Scrolling system log panel, styled like a terminal.
    Call .log("message") from anywhere in the app to append a line.
    """

    def __init__(self, parent=None, max_lines=200):
        super().__init__(parent)
        self.max_lines = max_lines
        self.setReadOnly(True)
        self.setStyleSheet(f"""
            QTextEdit {{
                background-color: {theme.CARD};
                border: 1px solid {theme.BORDER};
                border-radius: 6px;
                padding: 10px;
                color: {theme.TEXT_DIM};
                font-family: "Terminus (TTF)";
                font-size: 12px;
            }}
        """)
        self.log("System integrity check complete")
        self.log("FRIDAY CORE stable")

    def log(self, message: str):
        ts = QDateTime.currentDateTime().toString("hh:mm:ss")
        self.append(f"[{ts}] {message}")

        # trim old lines so it doesn't grow forever
        doc = self.document()
        if doc.blockCount() > self.max_lines:
            cursor = self.textCursor()
            cursor.movePosition(cursor.MoveOperation.Start)
            cursor.select(cursor.SelectionType.BlockUnderCursor)
            cursor.removeSelectedText()
            cursor.deleteChar()

        # auto-scroll to bottom
        sb = self.verticalScrollBar()
        sb.setValue(sb.maximum())