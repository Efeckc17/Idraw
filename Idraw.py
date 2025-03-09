# Copyright [2025] Toxi360
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys
import math
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QAction, QToolBar,
    QMessageBox, QInputDialog
)
from PyQt5.QtGui import QPainter, QPen, QColor, QPainterPath
from PyQt5.QtCore import Qt, QTimer, pyqtSignal

def generate_heart():
    steps = []
    scale = 15
    # Polar-based heart curve
    for i in range(629):
        t = i / 100
        x = 16 * (math.sin(t) ** 3)
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        steps.append((x * scale, -y * scale))
    return steps

def generate_rose():
    steps = []
    n = 800
    a = 150
    k = 4
    # r = a*sin(k*t)
    for i in range(n + 1):
        t = (2 * math.pi * i) / n
        r = a * math.sin(k * t)
        x = r * math.cos(t)
        y = r * math.sin(t)
        steps.append((x, y))
    return steps

def generate_lissajous():
    steps = []
    n = 800
    a1, b1 = 3, 2
    A, B = 150, 150
    delta = math.pi / 2
    for i in range(n + 1):
        t = (2 * math.pi * i) / n
        x = A * math.sin(a1 * t + delta)
        y = B * math.sin(b1 * t)
        steps.append((x, y))
    return steps

def generate_butterfly():
    steps = []
    n = 1000
    # x = sin(t)*( e^(cos t) - 2 cos(4t) - sin^5(t/12) ) * scale
    # y = cos(t)*( e^(cos t) - 2 cos(4t) - sin^5(t/12) ) * scale
    for i in range(n + 1):
        t = (12 * math.pi * i) / n
        e = math.exp(math.cos(t)) - 2 * math.cos(4 * t) - (math.sin(t / 12) ** 5)
        scale = 40
        x = math.sin(t) * e * scale
        y = math.cos(t) * e * scale
        steps.append((x, y))
    return steps

def generate_hypotrochoid():
    steps = []
    n = 1000
    R = 150
    r = 60
    d = 80
    # Hypotrochoid param: x = (R - r)*cos(t) + d*cos(((R - r)/r)*t)
    #                     y = (R - r)*sin(t) - d*sin(((R - r)/r)*t)
    for i in range(n + 1):
        t = (2 * math.pi * i) / n
        x = (R - r) * math.cos(t) + d * math.cos(((R - r) / r) * t)
        y = (R - r) * math.sin(t) - d * math.sin(((R - r) / r) * t)
        steps.append((x, y))
    return steps

def generate_epitrochoid():
    steps = []
    n = 1000
    R = 100
    r = 40
    d = 70
    # Epitrochoid param: x = (R + r)*cos(t) - d*cos(((R + r)/r)*t)
    #                    y = (R + r)*sin(t) - d*sin(((R + r)/r)*t)
    for i in range(n + 1):
        t = (2 * math.pi * i) / n
        x = (R + r) * math.cos(t) - d * math.cos(((R + r) / r) * t)
        y = (R + r) * math.sin(t) - d * math.sin(((R + r) / r) * t)
        steps.append((x, y))
    return steps

def generate_spiral():
    steps = []
    n = 1000
    a = 0
    b = 3
    # Archimedean Spiral: r = a + b*t
    # We'll let t vary from 0 to 4*pi for a few turns
    tmax = 4 * math.pi
    for i in range(n + 1):
        frac = i / n
        t = frac * tmax
        r = a + b * t
        x = r * math.cos(t)
        y = r * math.sin(t)
        steps.append((x, y))
    return steps

def generate_deltoid():
    steps = []
    n = 600
    R = 60
    # Deltoid param: x = 2R*cos(t) + R*cos(2t), y = 2R*sin(t) - R*sin(2t)
    for i in range(n + 1):
        t = (2 * math.pi * i) / n
        x = 2 * R * math.cos(t) + R * math.cos(2 * t)
        y = 2 * R * math.sin(t) - R * math.sin(2 * t)
        steps.append((x, y))
    return steps

def generate_astroid():
    steps = []
    n = 600
    a = 120
    # Astroid param: x = a*cos^3(t), y = a*sin^3(t)
    for i in range(n + 1):
        t = (2 * math.pi * i) / n
        x = a * (math.cos(t) ** 3)
        y = a * (math.sin(t) ** 3)
        steps.append((x, y))
    return steps

def generate_lemniscate():
    steps = []
    n = 1000
    a = 80
    # r^2 = a^2 cos(2t). We'll plot only where cos(2t) >= 0
    # x = r cos(t), y = r sin(t)
    for i in range(n + 1):
        t = 2 * math.pi * i / n
        c = math.cos(2 * t)
        if c >= 0:
            r = math.sqrt(a * a * c)
            x = r * math.cos(t)
            y = r * math.sin(t)
            steps.append((x, y))
    return steps

def generate_cochleoid():
    steps = []
    # r = a*sin(t) / t, let a=80
    # We'll skip t=0 to avoid singularity, and go from -2*pi to 2*pi
    a = 80
    n = 2000
    t_min, t_max = -2 * math.pi, 2 * math.pi
    for i in range(n + 1):
        frac = i / n
        t = t_min + (t_max - t_min) * frac
        # Avoid division by zero near t=0
        if abs(t) < 1e-4:
            continue
        r = (a * math.sin(t)) / t
        x = r * math.cos(t)
        y = r * math.sin(t)
        steps.append((x, y))
    return steps

def generate_fermat_spiral():
    steps = []
    # r^2 = a^2 * theta => r = a*sqrt(theta)
    # let a=10, theta from 0..6*pi
    a = 10
    n = 1000
    t_max = 6 * math.pi
    for i in range(n + 1):
        frac = i / n
        th = t_max * frac
        r = a * math.sqrt(th)
        x = r * math.cos(th)
        y = r * math.sin(th)
        steps.append((x, y))
    return steps

shape_map = {
    "Heart": generate_heart,
    "Rose": generate_rose,
    "Lissajous": generate_lissajous,
    "Butterfly": generate_butterfly,
    "Hypotrochoid": generate_hypotrochoid,
    "Epitrochoid": generate_epitrochoid,
    "Spiral": generate_spiral,
    "Deltoid": generate_deltoid,
    "Astroid": generate_astroid,
    "Lemniscate": generate_lemniscate,
    "Cochleoid": generate_cochleoid,
    "FermatSpiral": generate_fermat_spiral
}

class DrawingWidget(QWidget):
    exit_signal = pyqtSignal()
    def __init__(self, shape=None, speed=20, color=QColor("white"), parent=None):
        super().__init__(parent)
        self.shape_name = shape
        self.steps = []
        self.current_step = 0
        self.pen_color = color
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_drawing)
        self.speed = speed
        if shape:
            self.load_shape(shape)

    def load_shape(self, shape):
        self.shape_name = shape
        if shape in shape_map:
            self.steps = shape_map[shape]()
        else:
            self.steps = []
        self.current_step = 0
        if self.steps:
            self.timer.start(self.speed)
        else:
            self.timer.stop()

    def set_speed(self, ms):
        self.speed = ms
        self.timer.setInterval(self.speed)

    def set_color(self, color):
        self.pen_color = color

    def update_drawing(self):
        self.current_step += 1
        if self.current_step >= len(self.steps):
            self.current_step = 0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), Qt.black)

        if not self.steps:
            return

        cx = self.width() / 2
        cy = self.height() / 2
        path = QPainterPath()

        limit = min(self.current_step, len(self.steps))
        if limit > 0:
            x0, y0 = self.steps[0]
            path.moveTo(cx + x0, cy + y0)
            for i in range(1, limit):
                x, y = self.steps[i]
                path.lineTo(cx + x, cy + y)

        glow = QColor(self.pen_color)
        for i in range(5, 0, -1):
            glow.setAlpha(60)
            painter.setPen(QPen(glow, i * 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawPath(path)

        painter.setPen(QPen(self.pen_color, 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawPath(path)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_U:
            self.exit_signal.emit()

class ScreenSaverWindow(QMainWindow):
    def __init__(self, shape, speed, color, screen, parent=None):
        super().__init__(parent)
        self.shape = shape
        self.speed = speed
        self.color = color
        self.screen = screen
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setGeometry(self.screen.geometry())

        self.drawing_widget = DrawingWidget(shape, speed, color, self)
        self.drawing_widget.exit_signal.connect(parent.exit_screen_saver_mode)
        self.setCentralWidget(self.drawing_widget)
        self.showFullScreen()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Idraw")
        self.setGeometry(100, 100, 1200, 900)
        self.screen_saver_windows = []

        self.drawing_widget = DrawingWidget()
        self.setCentralWidget(self.drawing_widget)

        self.create_menu()

    def create_menu(self):
        toolbar = QToolBar("Shapes")
        self.addToolBar(toolbar)

        shapes = list(shape_map.keys())
        for shape in shapes:
            action = QAction(shape, self)
            action.triggered.connect(lambda _, s=shape: self.select_shape_normal_mode(s))
            toolbar.addAction(action)

        screensaver_action = QAction("Start Screen Saver", self)
        screensaver_action.triggered.connect(self.ask_screen_saver)
        toolbar.addAction(screensaver_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(QApplication.instance().quit)
        toolbar.addAction(exit_action)

    def select_shape_normal_mode(self, shape):
        color = self.select_color()
        if not color:
            return
        speed = self.select_speed()
        if not speed:
            return
        self.drawing_widget.load_shape(shape)
        self.drawing_widget.set_color(color)
        self.drawing_widget.set_speed(speed)

    def ask_screen_saver(self):
        answer = QMessageBox.question(
            self,
            "Screen Saver",
            "Do you want to enter screen saver mode?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if answer == QMessageBox.Yes:
            self.ask_shape_for_screensaver()

    def ask_shape_for_screensaver(self):
        shapes = list(shape_map.keys())
        shape, ok = QInputDialog.getItem(
            self, "Select Shape", "Which shape do you want?", shapes, 0, False
        )
        if ok and shape:
            color = self.select_color()
            if color:
                speed = self.select_speed()
                if speed:
                    self.enter_screen_saver_mode(shape, speed, color)

    def enter_screen_saver_mode(self, shape, speed, color):
        app = QApplication.instance()
        screens = app.screens()
        for screen in screens:
            window = ScreenSaverWindow(shape, speed, color, screen, self)
            self.screen_saver_windows.append(window)
        if self.screen_saver_windows:
            self.hide()

    def exit_screen_saver_mode(self):
        for window in self.screen_saver_windows:
            window.close()
        self.screen_saver_windows = []
        self.showNormal()

    def select_speed(self):
        speeds = ["Fast", "Normal", "Slow"]
        speed_map = {"Fast": 5, "Normal": 20, "Slow": 50}
        speed, ok = QInputDialog.getItem(
            self, "Select Speed", "Choose animation speed:", speeds, 1, False
        )
        if ok and speed:
            return speed_map[speed]
        return None

    def select_color(self):
        colors = [
            "Red", "Green", "Blue", "Yellow", "Cyan", "Magenta", "White",
            "Orange", "Purple", "Pink", "Gray", "Black"
        ]
        color_map = {
            "Red": QColor(255, 0, 0),
            "Green": QColor(0, 255, 0),
            "Blue": QColor(0, 0, 255),
            "Yellow": QColor(255, 255, 0),
            "Cyan": QColor(0, 255, 255),
            "Magenta": QColor(255, 0, 255),
            "White": QColor(255, 255, 255),
            "Orange": QColor(255, 165, 0),
            "Purple": QColor(128, 0, 128),
            "Pink": QColor(255, 192, 203),
            "Gray": QColor(128, 128, 128),
            "Black": QColor(0, 0, 0)
        }
        color, ok = QInputDialog.getItem(
            self, "Select Color", "Choose drawing color:", colors, 0, False
        )
        if ok and color:
            return color_map[color]
        return None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_U and self.screen_saver_windows:
            self.exit_screen_saver_mode()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
