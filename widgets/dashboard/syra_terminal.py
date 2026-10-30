from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QLineEdit,
)
from PyQt6.QtCore import Qt

from utils import theme


class FRIDAYTerminal(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        self.output.setStyleSheet(f"""
        QTextEdit{{
            background:#02060D;
            border:#008CFF;
            selection-background-color:#1EA7FF;
            selection-color:#05080F;
            color:{theme.TEXT_DIM};
            padding:15px;
            font-family:"Terminus (TTF)";
            font-size:13px;
        }}
        QScrollBar:vertical{{
            width:10px;
        }}

        QScrollBar:horizontal{{
            height:10;
        }}
        """)

        self.input = QLineEdit()

        self.input.setPlaceholderText("Type a command...")

        self.input.setStyleSheet(f"""
        QLineEdit{{
            background:{theme.CARD};
            border:{theme.BORDER};
            border-top:1px solid {theme.BORDER};
            padding:10px;
            color:{theme.TEXT};
            font-family:"Terminus (TTF)";
            font-size:13px;
        }}
        """)

        layout.addWidget(self.output)
        layout.addWidget(self.input)

        self.input.returnPressed.connect(self.execute_command)

        self.show_boot()
    
    def show_boot(self):

        self.print("> Booting FRIDAY Core...")
        self.print("> Loading Modules...")
        self.print("> Voice Engine ........ OFFLINE")
        self.print("> Scheduler ........... READY")
        self.print("> AI Core ............. IDLE")
        self.print("")
        self.output.insertHtml(
        f"""
        <br>
        <span style="color:{theme.TEXT_DIM};">
        Type
        </span>

        <span style="color:#8FD3FF;">
        help
        </span>

        <span style="color:{theme.TEXT_DIM};">
        to begin.
        </span>

        <br><br>

        <span style="color:{theme.TEXT_DIM};">V.Aryan</span>
        <span style="color:{theme.TEXT};">@</span>
        <span style="color:{theme.PRIMARY};">FRIDAY</span>
        <span style="color:{theme.TEXT};">:~$ </span>
        """
        )

    def print(self,text):
        self.output.append(text)
        self.scroll_bottom()


    #Execute commands

    def execute_command(self):

        cmd = self.input.text().strip()

        self.output.insertHtml(
            f"""
            <br>
            <span style="color:{theme.TEXT_DIM};">V.Aryan</span>
            <span style="color:{theme.TEXT};">@</span>
            <span style="color:{theme.PRIMARY};">FRIDAY</span>
            <span style="color:{theme.TEXT};">:~$ </span>
            <span style="color:#8FD3FF;">{cmd}</span>
            <br>
            """
        )
        self.input.clear()

        if cmd == "":
            return

        if cmd == "help":

            self.print("""
Available Commands

help
clear
status
projects
tasks
FRIDAYfetch
about
            """)

        elif cmd == "clear":

            self.output.clear()

        elif cmd == "status":

            self.print("""
FRIDAYAYAYAY STATUS

AI : Idle
Voice : Offline
Scheduler : Ready
            """)

        elif cmd == "about":

            self.print("""
FRIDAY v3.5.5

Smart
Yielding
Responsive
Assistant
            """)

        elif cmd == "FRIDAYfetch":

            self.FRIDAYfetch()

        else:

            self.print("Unknown command.")


#---------------------FRIDAYFETCH---------------------------
    def FRIDAYfetch(self):

        self.output.insertHtml(f"""
        <pre style="
        line-height:65%;
        font-family:'Terminus (TTF)';
        font-size:12px;
        margin:0;
        ">
        <span style="color:{theme.PRIMARY};">
        ███████╗██╗   ██╗██████╗  █████╗      </span><span style="color:{theme.TEXT_DIM};">User      :</span> <span style="color:{theme.TEXT};">_______</span>
        <span style="color:{theme.PRIMARY};">
        ██╔════╝╚██╗ ██╔╝██╔══██╗██╔══██╗     </span><span style="color:{theme.TEXT_DIM};">Core      :</span> <span style="color:{theme.PRIMARY};">FRIDAY v3.5.5</span>
        <span style="color:{theme.PRIMARY};">
        ███████╗ ╚████╔╝ ██████╔╝███████║     </span><span style="color:{theme.TEXT_DIM};">AI        :</span> <span style="color:#00FFAA;">Idle</span>
        <span style="color:{theme.PRIMARY};">
        ╚════██║  ╚██╔╝  ██╔══██╗██╔══██║     </span><span style="color:{theme.TEXT_DIM};">Voice     :</span> <span style="color:#FFC857;">Offline</span>
        <span style="color:{theme.PRIMARY};">
        ███████║   ██║   ██║  ██║██║  ██║     </span><span style="color:{theme.TEXT_DIM};">Engine    :</span> <span style="color:#00FFAA;">Ready</span>
        <span style="color:{theme.PRIMARY};">
        ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝     </span><span style="color:{theme.TEXT_DIM};">Terminal  :</span> <span style="color:#00FFAA;">Online</span>
        </pre>
        """)

        self.scroll_bottom()

    
    def scroll_bottom(self):

        bar = self.output.verticalScrollBar()

        bar.setValue(bar.maximum())