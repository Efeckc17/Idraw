import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QAction, QToolBar, QMessageBox, QInputDialog
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QPainterPath
from PyQt5.QtCore import Qt, QPointF, QTimer, pyqtSignal

def generate_heart():
    steps = []
    scale = 15
    for i in range(0, 628, 2):
        t = i / 100
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        steps.append((x * scale, -y * scale))
    return steps

def generate_spiral():
    steps = []
    turns = 10
    points = 3000
    max_radius = 400
    for i in range(points):
        theta = i * turns * 2 * math.pi / points
        r = max_radius * theta / (turns * 2 * math.pi)
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        steps.append((x, y))
    return steps

def generate_star():
    steps = []
    outer = 200
    inner = 90
    n = 5
    for i in range(n * 2 + 1):
        angle = i * math.pi / n
        r = outer if i % 2 == 0 else inner
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        steps.append((x, y))
    return steps

def generate_flower():
    steps = []
    petals = 12
    radius = 300
    for i in range(petals * 2 + 1):
        angle = i * math.pi / petals
        r = radius * math.sin(angle)
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        steps.append((x, y))
    for i in range(0, 628, 8):
        t = i / 100
        x = 100 * math.cos(t)
        y = 100 * math.sin(t)
        steps.append((x, y))
    return steps

def generate_moon():
    steps = []
    r = 150
    for i in range(0, 628, 2):
        t = i / 100
        x = r * math.cos(t)
        y = r * math.sin(t)
        steps.append((x, y))
    offset = 80
    for i in range(0, 314, 2):
        t = i / 100
        x = (r - offset) * math.cos(t)
        y = (r - offset) * math.sin(t)
        steps.append((x, y))
    return steps

def generate_sun():
    steps = []
    radius = 180
    for i in range(0, 628, 2):
        t = i / 100
        x = radius * math.cos(t)
        y = radius * math.sin(t)
        steps.append((x, y))
    for angle in range(0, 360, 10):
        rad = math.radians(angle)
        for r in range(radius, radius + 90, 5):
            x = r * math.cos(rad)
            y = r * math.sin(rad)
            steps.append((x, y))
    return steps

def generate_cloud():
    steps = []
    ellipses = [
        (-170, 0, 140, 90),
        (-80, -50, 180, 110),
        (40, 0, 140, 90),
        (140, -50, 180, 110),
        (250, 0, 140, 90),
    ]
    for ex, ey, ew, eh in ellipses:
        for i in range(0, 628, 10):
            t = i / 100
            x = ew * math.cos(t)
            y = eh * math.sin(t)
            steps.append((ex + x, ey + y))
    return steps

def generate_tree():
    steps = []
    width_ = 50
    height_ = 350
    for y in range(0, height_, 3):
        steps.append((-width_ / 2, -y))
        steps.append((width_ / 2, -y))
    foliage = 180
    for i in range(0, 628, 2):
        t = i / 100
        x = foliage * math.cos(t)
        y = foliage * math.sin(t) - height_
        steps.append((x, y))
    return steps

def generate_elephant():
    steps = []
    sc = 2.5
    for i in range(0, 628, 8):
        t = i / 100
        x = 110 * math.cos(t)
        y = 60 * math.sin(t)
        steps.append((x * sc, y * sc))
    for i in range(0, 628, 8):
        t = i / 100
        x = 35 * math.cos(t)
        y = 25 * math.sin(t) - 30 * sc
        steps.append(((110 + x) * sc, y * sc))
    for i in range(0, 200, 4):
        t = i / 100
        steps.append(((150) * sc, (-30 + 60 * t) * sc))
    return steps

def generate_bird():
    steps = []
    sc = 2
    for i in range(0, 628, 8):
        t = i / 100
        x = 50 * math.cos(t)
        y = 25 * math.sin(t)
        steps.append((x * sc, y * sc))
    for i in range(0, 628, 8):
        t = i / 100
        x = 60 * math.cos(t)
        y = 25 * math.sin(t)
        steps.append(((x - 25) * sc, y * sc))
        steps.append(((x + 25) * sc, y * sc))
    for i in range(0, 100, 5):
        t = i / 100
        x = 70 + i * 0.5
        y = 15 * math.sin(t)
        steps.append((x * sc, y * sc))
    return steps

shape_map = {
    "Heart": generate_heart,
    "Spiral": generate_spiral,
    "Star": generate_star,
    "Flower": generate_flower,
    "Moon": generate_moon,
    "Sun": generate_sun,
    "Cloud": generate_cloud,
    "Tree": generate_tree,
    "Elephant": generate_elephant,
    "Bird": generate_bird
}

class DrawingWidget(QWidget):
    exit_signal = pyqtSignal()
    def __init__(self, shape, speed, color, parent=None):
        super(DrawingWidget, self).__init__(parent)
        self.shape_name = shape
        self.steps = []
        self.current_step = 0
        self.pen_color = color
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_drawing)
        self.speed = speed
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
    
    def update_drawing(self):
        self.current_step += 1
        if self.current_step >= len(self.steps):
            self.current_step = 0
    
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor("black"))
        if not self.steps:
            return
        pen = QPen(self.pen_color, 3)
        painter.setPen(pen)
        painter.setBrush(QBrush(self.pen_color))
        cx = self.width() / 2
        cy = self.height() / 2
        path = QPainterPath()
        if self.current_step > 0:
            x0, y0 = self.steps[0]
            path.moveTo(cx + x0, cy + y0)
            for i in range(1, min(self.current_step, len(self.steps))):
                x, y = self.steps[i]
                path.lineTo(cx + x, cy + y)
            painter.drawPath(path)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_U:
            self.exit_signal.emit()

class ScreenSaverWindow(QMainWindow):
    def __init__(self, shape, speed, color, screen, parent=None):
        super(ScreenSaverWindow, self).__init__(parent)
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
        super(MainWindow, self).__init__()
        self.setWindowTitle("Idraw")
        self.setGeometry(100, 100, 1200, 900)
        self.screen_saver_windows = []
        self.create_menu()
        self.ask_screen_saver()
    
    def create_menu(self):
        toolbar = QToolBar("Shapes")
        self.addToolBar(toolbar)
        shapes = list(shape_map.keys())
        for shape in shapes:
            action = QAction(shape, self)
            action.triggered.connect(lambda checked, s=shape: self.select_shape(s))
            toolbar.addAction(action)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(QApplication.instance().quit)
        toolbar.addAction(exit_action)
    
    def select_shape(self, shape):
        color = self.select_color()
        if color:
            speed = self.select_speed()
            if speed:
                self.enter_screen_saver_mode(shape, speed, color)
    
    def ask_screen_saver(self):
        answer = QMessageBox.question(self, "Screen Saver", "Do you want to enter screen saver mode?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if answer == QMessageBox.Yes:
            self.ask_shape()
    
    def ask_shape(self):
        shapes = list(shape_map.keys())
        shape, ok = QInputDialog.getItem(self, "Select Shape", "Which shape do you want?", shapes, 0, False)
        if ok and shape:
            color = self.select_color()
            if color:
                speed = self.select_speed()
                if speed:
                    self.enter_screen_saver_mode(shape, speed, color)
    
    def select_speed(self):
        speeds = ["Fast", "Normal", "Slow"]
        speed_map = {"Fast": 5, "Normal": 20, "Slow": 50}
        speed, ok = QInputDialog.getItem(self, "Select Speed", "Choose animation speed:", speeds, 1, False)
        if ok and speed:
            return speed_map[speed]
        return None
    
    def select_color(self):
        colors = ["Red", "Green", "Blue", "Yellow", "Cyan", "Magenta", "White"]
        color_map = {
            "Red": QColor(255, 0, 0),
            "Green": QColor(0, 255, 0),
            "Blue": QColor(0, 0, 255),
            "Yellow": QColor(255, 255, 0),
            "Cyan": QColor(0, 255, 255),
            "Magenta": QColor(255, 0, 255),
            "White": QColor(255, 255, 255)
        }
        color, ok = QInputDialog.getItem(self, "Select Color", "Choose drawing color:", colors, 0, False)
        if ok and color:
            return color_map[color]
        return None
    
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
