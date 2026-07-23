import psutil

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
)

from utils import theme


class SystemMonitor(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(12, 12, 12, 12)

        title = QLabel("SYSTEM MONITOR")
        title.setStyleSheet(f"""
            font-size:16px;
            font-weight:bold;
            color:{theme.TEXT_SECONDARY};
            letter-spacing:2px;
            border:none;
        """)

        layout.addWidget(title)

        self.cpu = self.create_row("CPU")
        self.ram = self.create_row("RAM")
        self.disk = self.create_row("DISK")
        self.battery = self.create_row("BATTERY")
        self.network = self.create_row("NETWORK")
        self.uptime = self.create_row("UPTIME")
        self.temperature = self.create_row("TEMPERATURE")

        layout.addStretch()

        self.setStyleSheet(f"""
        QWidget {{
            background:{theme.CARD};
            border:1px solid {theme.BORDER};
            border-radius:8px;
        }}
        """)
        self.cpu_history = []
        self.net_history = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_monitor)
        self.timer.start(1000)

        self.update_monitor()


    def create_row(self, title):

        frame = QFrame()

        frame.setStyleSheet("border:none;")

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(6,6,6,6)
        layout.setSpacing(4)

        label = QLabel(title)
        label.setStyleSheet(f"""
            color:{theme.TEXT_DIM};
            font-size:12px;
            border:none;
        """)

        value = QLabel("--")
        value.setStyleSheet(f"""
        color:{theme.TEXT_DIM};
        font-family:"JetBrains Mono";
        font-size:12px;
        font-weight:bold;
        border:none;
        """)

        layout.addWidget(label)
        layout.addWidget(value)

        self.layout().addWidget(frame)

        return value
    
    def make_bar(self, value, total=14):
        filled = int((value / 100) * total)
        return "█" * filled + "░" * (total - filled)


    def make_blocks(self, value, total=8):
        filled = int((value / 100) * total)
        return "■" * filled + "□" * (total - filled)
    

    def lines(self, values):
        chars = "၊|│|၊|│|၊|│|၊|│|၊"

        if not values:
            return ""
        maximum = max(values)
        if maximum == 0:
            maximum = 1
        return "".join(
            chars[min(7, int(v / maximum * 7))]
            for v in values
        )


    def sparkline(self, values):
        chars = "▁▂▃▄▅▆▇█"

        if not values:
            return ""

        maximum = max(values)

        if maximum == 0:
            maximum = 1

        return "".join(
            chars[min(7, int(v / maximum * 7))]
            for v in values
        )
    
    def update_monitor(self):

        # CPU
        cpu = psutil.cpu_percent(interval=None)

        cpu_bar = self.make_bar(cpu)

        self.cpu.setText(
            f"{cpu_bar}\n{cpu:.0f}%"
        )

        # RAM
        ram = psutil.virtual_memory().percent

        ram_bar = self.make_blocks(ram)

        self.ram.setText(
            f"{ram_bar}\n{ram:.0f}%"
        )

        # Disk
        disk = psutil.disk_usage("/").percent

        disk_bar = self.make_blocks(disk)

        self.disk.setText(
            f"{disk_bar}\n{disk:.0f}%"
        )

        # Battery
        battery = psutil.sensors_battery()
        battery_bar = self.make_blocks(battery.percent)

        if battery:

            charging = "⚡ " if battery.power_plugged else ""

            self.battery.setText(
                f"{battery_bar}\n{charging}{battery.percent:.0f}%"
            )

        else:

            self.battery.setText("--")

        # Network

        net = psutil.net_io_counters()

        sent = net.bytes_sent / (1024 * 1024)

        recv = net.bytes_recv / (1024 * 1024)

        speed = recv

        self.net_history.append(speed)

        if len(self.net_history) > 20:
            self.net_history.pop(0)

        graph = self.lines(self.net_history)

        self.network.setText(
            f"↑ {sent:.1f} MB\n"
            f"↓ {recv:.1f} MB\n"
            f"{graph}"
        )

        # Uptime

        import time

        uptime = int(time.time() - psutil.boot_time())

        hours = uptime // 3600

        mins = (uptime % 3600) // 60

        self.uptime.setText(f"{hours}h {mins}m")

        # Temperature

        try:

            temps = psutil.sensors_temperatures()

            if temps:

                first = next(iter(temps.values()))

                self.temperature.setText(
                    f"{first[0].current:.1f}°C"
                )

            else:

                self.temperature.setText("--")

        except:

            self.temperature.setText("--")