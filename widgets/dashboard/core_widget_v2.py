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

    __slots__ = (
    "widget",

    "theta",
    "phi",
    "radius",

    "vx",
    "vy",
    "vz",

    "size",
    "brightness",

    "age",
    "life",
    )

    def __init__(self, widget):

        self.widget = widget

        self.theta = random.uniform(0, math.pi * 2)
        self.phi = math.acos(random.uniform(-1, 1))

        self.radius = random.uniform(0.02, 0.10)

        x = math.sin(self.phi) * math.cos(self.theta)
        y = math.sin(self.phi) * math.sin(self.theta)
        z = math.cos(self.phi)

        speed = random.uniform(
            widget.emit_speed_min,
            widget.emit_speed_max
        )

        self.vx = x * speed
        self.vy = y * speed
        self.vz = z * speed

        self.size = random.uniform(
            widget.particle_size_min,
            widget.particle_size_max
        )

        self.brightness = random.uniform(
            widget.brightness_min,
            widget.brightness_max
        )

        self.life = random.randint(120, 220)
        self.age = 0

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

        # =====================
        # CORE SETTINGS
        # =====================

        # Particle cloud size
        self.cloud_radius = 1.0

        # Number of particles
        self.point_count = point_count

        # Rotation speed
        self.rotation_speed = 0.5

        # Particle outward speed
        self.emit_speed_min = 0.005
        self.emit_speed_max = 0.01

        # Particle size
        self.particle_size_min = 1.2
        self.particle_size_max = 2.6

        # Brightness
        self.brightness_min = 0.45
        self.brightness_max = 1.0

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
            p = SpherePoint(self)

            # Randomize age so the cloud starts already "alive"
            p.age = random.randint(0, p.life)

            self.points.append(p)


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

        self.global_angle += self.rotation_speed

        # Spawn new particles continuously
        for _ in range(20):
            self.points.append(SpherePoint(self))

        alive = []

        for p in self.points:

            p.age += 1

            p.radius += math.sqrt(
                p.vx * p.vx +
                p.vy * p.vy +
                p.vz * p.vz
            )

            if p.age < p.life and p.radius < 1.2:
                alive.append(p)

        self.points = alive

        # Prevent unlimited growth
        if len(self.points) > 4500:
            self.points = self.points[-4500:]

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
            direction_x = math.sin(p.phi) * math.cos(p.theta)
            direction_y = math.sin(p.phi) * math.sin(p.theta)
            direction_z = math.cos(p.phi)

            x = direction_x * p.radius * self.cloud_radius
            y = direction_y * p.radius * self.cloud_radius
            z = direction_z * p.radius * self.cloud_radius

            rx, ry, rz = rotate_point(
                x,
                y,
                z,
                0.15,
                ga,
                0
            )
            scale = focal / (focal + rz * R)
            sx = cx + rx * R * scale
            sy = cy + ry * R * scale
            projected.append((rz, sx, sy, p.size, p.brightness, scale, p))

        projected.sort(key=lambda item: item[0])

        for rz, sx, sy, size, brightness, scale, p in projected:

            depth_factor = (rz + 1) / 2  # 0 = back, 1 = front

            life_progress = p.age / p.life

            if life_progress < 0.2:
                fade = life_progress / 0.2

            elif life_progress > 0.8:
                fade = (1 - life_progress) / 0.2

            else:
                fade = 1

            alpha = int(
                255 *
                p.brightness *
                fade *
                (0.25 + depth_factor * 0.75)
            )

            alpha = max(10, min(alpha, 255))

           
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