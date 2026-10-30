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

    "speed",
    "dir_x",
    "dir_y",
    "dir_z",

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

        self.dir_x = math.sin(self.phi) * math.cos(self.theta)
        self.dir_y = math.sin(self.phi) * math.sin(self.theta)
        self.dir_z = math.cos(self.phi)

        self.speed = random.uniform(
            widget.emit_speed_min,
            widget.emit_speed_max
        )

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
    __slots__ = (
        "radius", 
        "tilt_x", 
        "tilt_y", 
        "tilt_z", 
        "spin_speed", 
        "phase", 
        "width", 
        "color",
        "node_phase"
        )

    def __init__(self, radius, tilt_x, tilt_y, tilt_z, spin_speed, width, color):
        self.radius = radius
        self.tilt_x = tilt_x
        self.tilt_y = tilt_y
        self.tilt_z = tilt_z
        self.spin_speed = spin_speed
        self.phase = 0.0
        self.width = width
        self.color = color
        self.node_phase = random.uniform(0, math.pi * 2)

class EnergyPulse:

    def __init__(self):

        self.radius = 0.05

        self.alpha = 180

        self.speed = 0.018


class CoreWidget(QWidget):
    """
    3D particle-sphere core with independently tilted, independently
    spinning orbital rings — atom / arc-reactor style.
    """

    def __init__(self, parent=None, point_count=2500, ring_count=4):
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
        self.energy_pulses = []

        self._build_particle_cloud(point_count)
        self._build_rings(ring_count)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(30)  # ~33fps

        self.spawn_rate = 20
        self.max_particles = 4500
        self.max_radius = 1.2
        self.fade_in = 0.2
        self.fade_out = 0.8

    def _build_particle_cloud(self, count):

        self.points = []

        for _ in range(count):
            p = SpherePoint(self)

            # Randomize age so the cloud starts already "alive"
            p.age = random.randint(0, p.life)

            self.points.append(p)


    def _build_rings(self, count):
        configs = [
            (0.88, 25, 10, 0, 0.035),
            (0.95, -30, 55, 0, -0.030),
            (1.02, 70, -20, 0, 0.025),
            (0.82, 0, 80, 0, -0.020),
        ]

        colors = [
            "#1EA7FF",
            "#5FC7FF",
            "#1EA7FF",
            "#5FC7FF",
        ]

        for i in range(len(configs)):
            r, tx, ty, tz, speed = configs[i]

            self.rings.append(
                OrbitRing(
                    r,
                    math.radians(tx),
                    math.radians(ty),
                    math.radians(tz),
                    speed,
                    0.7,
                    colors[i]
                )
            )
    def _tick(self):

        self.global_angle += self.rotation_speed

        # Spawn new particles continuously
        for _ in range(self.spawn_rate):
            self.points.append(SpherePoint(self))

        alive = []

        for p in self.points:

            p.age += 1

            p.radius += p.speed

            if p.age < p.life and p.radius < self.max_radius:
                alive.append(p)

        self.points = alive

        # Prevent unlimited growth
        if len(self.points) > self.max_particles:
            self.points = self.points[-4500:]

        for ring in self.rings:
            ring.phase += ring.spin_speed
            ring.node_phase += ring.spin_speed * 1.8

        # Spawn pulse every ~1.5 sec

        if random.randint(0, 45) == 0:
            self.energy_pulses.append(EnergyPulse())

        alive = []

        for pulse in self.energy_pulses:

            pulse.radius += pulse.speed

            pulse.alpha -= 3

            if pulse.alpha > 0:
                alive.append(pulse)

        self.energy_pulses = alive

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
            painter.setBrush(Qt.BrushStyle.NoBrush)
            # layered glow: wide+faint underneath, narrow+bright on top
            for width_mult, alpha in (
                (5.0, 25), 
                (3.0, 45), 
                (1.6, 90), 
                (1.0, 200)
                ):
                c = QColor(base_color)
                c.setAlpha(alpha)
                pen = QPen(c)
                pen.setWidthF(ring.width * width_mult)
                pen.setCapStyle(Qt.PenCapStyle.RoundCap)
                painter.setPen(pen)
                painter.drawPath(path)

            # -----------------------------
            # Orbit Energy Node
            # -----------------------------

            t = ring.node_phase

            ux = ring.radius * math.cos(t)
            uy = ring.radius * math.sin(t)
            uz = 0

            rx, ry, rz = rotate_point(
                ux,
                uy,
                uz,
                ring.tilt_x,
                ring.tilt_y + ring.phase,
                ring.tilt_z
            )

            rx, ry, rz = rotate_point(
                rx,
                ry,
                rz,
                0,
                ga,
                0
            )

            scale = focal / (focal + rz * R)

            sx = cx + rx * R * scale
            sy = cy + ry * R * scale

            # glow

            for radius, alpha in (
                (12,20),
                (8,40),
                (5,90),
            ):

                c = QColor(40,180,255,alpha)

                painter.setBrush(c)

                painter.setPen(Qt.PenStyle.NoPen)

                painter.drawEllipse(
                    QPointF(sx,sy),
                    radius * scale,
                    radius * scale
                )

            # center

            painter.setBrush(QColor("#FFFFFF"))

            painter.drawEllipse(
                QPointF(sx,sy),
                2.5,
                2.5
            )


        # ---------- ENERGY PULSES ----------

        for pulse in self.energy_pulses:

            radius = pulse.radius * R

            color = QColor(40,180,255,pulse.alpha)

            pen = QPen(color)

            pen.setWidthF(2)

            painter.setPen(pen)

            painter.setBrush(Qt.BrushStyle.NoBrush)

            painter.drawEllipse(
                QPointF(cx,cy),
                radius,
                radius
            )
                

        # ---- sphere particles, depth-sorted back to front ----
        projected = []
        for p in self.points:
            x = p.dir_x * p.radius * self.cloud_radius
            y = p.dir_y * p.radius * self.cloud_radius
            z = p.dir_z * p.radius * self.cloud_radius

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

            if life_progress < self.fade_in:
                fade = life_progress / self.fade_in

            elif life_progress > self.fade_out:
                fade = (1 - life_progress) / (1 - self.fade_out)

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