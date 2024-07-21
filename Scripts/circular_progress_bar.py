import sys
import os
from math import cos, sin, radians
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def get_angle(hour, minute=0):
    """
    Converts a given hour (and optional minute) into the corresponding angle for the progress bar.

    Args:
        hour (int): The hour on the clock (0-11).
        minute (int, optional): The minutes past the hour (0-59). Defaults to 0.

    Returns:
        float: The angle in degrees.
    """
    hour = hour % 12
    angle_deg = (hour * 30) + (minute * 0.5)
    return angle_deg - 90

class CircularProgress(QWidget):
    def __init__(self, start_angle, end_angle):
        super().__init__()
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.width = 400
        self.height = 400
        self.progress_width = 30
        self.progress_rounded_cap = True
        self.progress_color = QColor(22, 109, 245)
        self.background_color = QColor(220, 220, 220)
        self.font_family = "Segoe UI"
        self.font_size = 12
        self.text_color = QColor(0, 0, 0)
        self.resize(self.width, self.height)

        this_file_location = os.path.dirname(__file__)
        center_image = os.path.abspath(os.path.join(this_file_location, '..', 'Images', 'bg.png'))
        start_image = os.path.abspath(os.path.join(this_file_location, '..', 'Images', 'profile_white.png'))
        end_image = os.path.abspath(os.path.join(this_file_location, '..', 'Images', 'time-left (1).png'))
        self.center_image = QImage(center_image)
        self.start_image = QImage(start_image)
        self.end_image = QImage(end_image)

        self.start_image = self.start_image.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.end_image = self.end_image.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def add_shadow(self, enable):
        if enable:
            self.shadow = QGraphicsDropShadowEffect(self)
            self.shadow.setBlurRadius(15)
            self.shadow.setXOffset(0)
            self.shadow.setYOffset(0)
            self.shadow.setColor(QColor(0, 0, 0, 120))
            self.setGraphicsEffect(self.shadow)

    def paintEvent(self, e):
        size = min(self.width, self.height)
        width = int(size - self.progress_width)
        height = int(size - self.progress_width)
        margin = int(self.progress_width / 2)

        # Calculate the arc length between the start and end angles
        angle_length = self.end_angle - self.start_angle
        if angle_length < 0:
            angle_length += 360

        paint = QPainter()
        paint.begin(self)
        paint.setRenderHint(QPainter.Antialiasing)
        font = QFont(self.font_family, self.font_size, QFont.Bold)
        paint.setFont(font)

        rect = QRect(0, 0, size, size)
        paint.setPen(Qt.NoPen)
        paint.drawRect(rect)

        # Draw the background circle (uncompleted part)
        pen = QPen()
        pen.setColor(self.background_color)
        pen.setWidth(self.progress_width)
        if self.progress_rounded_cap:
            pen.setCapStyle(Qt.RoundCap)
        paint.setPen(pen)
        paint.drawArc(margin, margin, width, height, 0, 360 * 16)

        # Draw the progress bar (completed part)
        pen.setColor(self.progress_color)
        paint.setPen(pen)
        paint.drawArc(margin, margin, width, height, int(self.start_angle * 16), - int(angle_length * 16))

        # Draw the center image
        image_size = size - self.progress_width * 2
        scaled_center_image = self.center_image.scaled(image_size, image_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_rect = QRect(margin + self.progress_width // 2, margin + self.progress_width // 2, image_size, image_size)
        paint.drawImage(image_rect, scaled_center_image)

        # Draw start image
        start_angle_rad = radians(self.start_angle)
        start_x = int(size / 2 + (width / 2) * cos(start_angle_rad) - self.start_image.width() / 2)
        start_y = int(size / 2 + (height / 2) * sin(start_angle_rad) - self.start_image.height() / 2)
        paint.drawImage(QRect(start_x, start_y, self.start_image.width(), self.start_image.height()), self.start_image)

        # Draw end image
        end_angle_rad = radians(self.end_angle)
        end_x = int(size / 2 + (width / 2) * cos(end_angle_rad) - self.end_image.width() / 2)
        end_y = int(size / 2 + (height / 2) * sin(end_angle_rad) - self.end_image.height() / 2)
        paint.drawImage(QRect(end_x, end_y, self.end_image.width(), self.end_image.height()), self.end_image)

        paint.end()

class MainWindow(QMainWindow):
    def __init__(self, start_angle, end_angle):
        super().__init__()
        self.resize(600, 600)

        self.container = QFrame()
        self.container.setStyleSheet("background-color: white")
        self.layout = QVBoxLayout()

        self.progress = CircularProgress(start_angle, end_angle)
        self.progress.suffix = "%"
        self.progress.font_size = 30
        self.progress.width = 500
        self.progress.height = 500
        self.progress.progress_width = 40
        self.progress.progress_color = QColor(22, 109, 245)
        self.progress.progress_rounded_cap = True
        self.progress.setMinimumSize(self.progress.width, self.progress.height)

        self.layout.addWidget(self.progress, Qt.AlignCenter, Qt.AlignCenter)

        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.show()

if __name__ == "__main__":
    start_hour = int(input("Enter the start hour for the progress bar (0-11): "))
    end_hour = int(input("Enter the end hour for the progress bar (0-11): "))
    start_angle = get_angle(start_hour)
    end_angle = get_angle(end_hour)

    app = QApplication(sys.argv)
    window = MainWindow(start_angle, end_angle)
    sys.exit(app.exec_())
