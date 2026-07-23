import math
import random
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QPainter, QColor, QRadialGradient, QBrush, QPen, QPainterPath


def rotate_point(x, y, z, ax, ay, az):
    """Rotate a 3D point around X, then Y, then Z axes (radians)."""
    cosx, sinx = math.cos(ax), math.sin(ax)
    y, z = y * cosx - z * sinx, y * sinx + z * cosx

    cosy, siny = math.cos(ay), math.sin(ay)
    x, z = x * cosy + z * siny, -x * siny + z * cosy

    cosz, sinz = math.cos(az), math.sin(az)
    x, y = x * cosz - y * sinz, x * sinz + y * cosz

    return x, y, z


class SpherePoint:
    __slots__ = ("x0", "y0", "z0", "size", "brightness")

    def __init__(self, x0, y0, z0, size, brightness):
        self.x0, self.y0, self.z0 = x0, y0, z0
        self.size = size
        self.brightness = brightness


class OrbitRing:
    __slots__ = ("radius", "tilt_x", "tilt_y", "tilt_z", "spin_speed", "phase", "width", "color")

    def __init__(self, radius, tilt_x, tilt_y, tilt_z, spin_speed, width, color):
        self.radius = radius
        self.tilt_x = tilt_x
        self.tilt_y = tilt_y
        self.tilt_z = tilt_z
        self.spin_speed = spin_speed
        self.phase = 0.0
        self.width = width
        self.color = color


class CoreWidget(QWidget):
    """
    3D particle-sphere core with independently tilted, independently
    spinning orbital rings — atom / arc-reactor style.
    """

    def __init__(self, parent=None, point_count=3500, ring_count=5):
        super().__init__(parent)
        self.setMinimumSize(350, 350)

        self.global_angle = 0.0
        self.points = []
        self.rings = []

        self._build_particle_cloud(point_count)
        self._build_rings(ring_count)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(30)  # ~33fps

    def _build_particle_cloud(self, count):

        self.points = []

        for _ in range(count):

            theta = random.uniform(0, math.pi * 2)

            phi = math.acos(random.uniform(-1, 1))

            # Much denser near outer shell
            r = random.uniform(0.72, 1.0)

            x = r * math.sin(phi) * math.cos(theta)
            y = r * math.sin(phi) * math.sin(theta)
            z = r * math.cos(phi)

            size = random.uniform(0.8, 2.0)

            brightness = random.uniform(0.35, 1.0)

            self.points.append(
                SpherePoint(
                    x,
                    y,
                    z,
                    size,
                    brightness
                )
            )

    def _build_rings(self, count):
        colors = ["#1EA7FF", "#5FC7FF", "#7FD4FF", "#39B6FF"]
        for _ in range(count):
            radius = random.uniform(0.78, 1.05)
            tilt_x = random.uniform(0, math.pi)
            tilt_y = random.uniform(0, math.pi)
            tilt_z = random.uniform(0, math.pi)
            spin_speed = random.uniform(0.03, 0.11) * random.choice([-1, 1])
            width = random.uniform(1.2, 2.0)
            color = random.choice(colors)
            self.rings.append(OrbitRing(radius, tilt_x, tilt_y, tilt_z, spin_speed, width, color))

    def _tick(self):
        self.global_angle += 0.4
        for ring in self.rings:
            ring.phase += ring.spin_speed
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        cx, cy = w / 2, h / 2
        R = min(w, h) / 2 - 20
        focal = R * 2.6
        ga = math.radians(self.global_angle)

        # ---- background glow ----
        glow = QRadialGradient(cx, cy, R * 1.3)
        glow.setColorAt(0.0, QColor(30, 167, 255, 50))
        glow.setColorAt(0.55, QColor(30, 167, 255, 15))
        glow.setColorAt(1.0, QColor(5, 8, 15, 0))
        painter.setBrush(QBrush(glow))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(int(cx - R * 1.3), int(cy - R * 1.3), int(R * 2.6), int(R * 2.6))

        # ---- outer dashed containment circle ----
        dash_pen = QPen(QColor(30, 167, 255, 70))
        dash_pen.setStyle(Qt.PenStyle.DashLine)
        painter.setPen(dash_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(int(cx - R * 1.25), int(cy - R * 1.25), int(R * 2.5), int(R * 2.5))

        # ---- orbit rings ----
        for ring in self.rings:
            pts2d = []
            segs = 72
            for s in range(segs + 1):
                t = (s / segs) * math.pi * 2
                ux = ring.radius * math.cos(t)
                uy = ring.radius * math.sin(t)
                uz = 0.0
                rx, ry, rz = rotate_point(ux, uy, uz, ring.tilt_x, ring.tilt_y + ring.phase, ring.tilt_z)
                rx, ry, rz = rotate_point(rx, ry, rz, 0, ga, 0)
                scale = focal / (focal + rz * R)
                sx = cx + rx * R * scale
                sy = cy + ry * R * scale
                pts2d.append((sx, sy))

            path = QPainterPath()
            path.moveTo(*pts2d[0])
            for sx, sy in pts2d[1:]:
                path.lineTo(sx, sy)

            base_color = QColor(ring.color)
            # layered glow: wide+faint underneath, narrow+bright on top
            for width_mult, alpha in ((5.0, 25), (3.0, 45), (1.6, 90), (1.0, 200)):
                c = QColor(base_color)
                c.setAlpha(alpha)
                pen = QPen(c)
                pen.setWidthF(ring.width * width_mult)
                pen.setCapStyle(Qt.PenCapStyle.RoundCap)
                painter.setPen(pen)
                painter.drawPath(path)

        # ---- sphere particles, depth-sorted back to front ----
        projected = []
        for p in self.points:
            rx, ry, rz = rotate_point(p.x0, p.y0, p.z0, 0.15, ga, 0)
            scale = focal / (focal + rz * R)
            sx = cx + rx * R * scale
            sy = cy + ry * R * scale
            projected.append((rz, sx, sy, p.size, p.brightness, scale))

        projected.sort(key=lambda item: item[0])

        for rz, sx, sy, size, brightness, scale in projected:
            depth_factor = (rz + 1) / 2  # 0 = back, 1 = front
            alpha = max(15, min(255, int(255 * brightness * (0.25 + 0.75 * depth_factor))))
            color = QColor("#9FE0FF")
            color.setAlpha(alpha)
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            s = size * scale * (0.6 + 0.6 * depth_factor)
            painter.drawEllipse(QPointF(sx, sy), s / 2, s / 2)

        # ---- bright center core ----
        core_glow = QRadialGradient(cx, cy, 26)
        core_glow.setColorAt(0.0, QColor(230, 248, 255, 255))
        core_glow.setColorAt(0.4, QColor(30, 167, 255, 190))
        core_glow.setColorAt(1.0, QColor(30, 167, 255, 0))
        painter.setBrush(QBrush(core_glow))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(int(cx - 26), int(cy - 26), 52, 52)

        painter.setBrush(QBrush(QColor("#FFFFFF")))
        painter.drawEllipse(int(cx - 3), int(cy - 3), 6, 6)

        painter.end()
