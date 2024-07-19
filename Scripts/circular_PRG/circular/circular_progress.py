from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class CircularProgress(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        # CUSTOM PROPERTIES
        self.value = 0
        self.width = 500  # Increased width for larger radius
        self.height = 500  # Increased height for larger radius
        self.progress_width = 40  # Increased width for thicker bar
        self.progress_rounded_cap = True  # Set round cap for the progress bar
        self.progress_color =  QColor(22, 109, 245)  # Blue color similar to the image
        self.max_value = 100
        self.font_family = "Segoe UI"
        self.font_size = 12
        self.suffix = "%"
        self.text_color = 0xFFFFFF  # White text color for percentage
        # SET DEFAULT SIZE WITHOUT LAYOUT
        self.resize(self.width, self.height)
        
        # Load the image
        self.image = QImage(r'C:\Users\pande\OneDrive\Desktop\PyQt\Samadhan-App\Images\24-hours (1).png')  # Adjust path accordingly

    # ADD DROPSHADOW
    def add_shadow(self, enable):
        if enable:
            self.shadow = QGraphicsDropShadowEffect(self)
            self.shadow.setBlurRadius(15)
            self.shadow.setXOffset(0)
            self.shadow.setYOffset(0)
            self.shadow.setColor(QColor(0, 0, 0, 120))
            self.setGraphicsEffect(self.shadow)

    # PAINT EVENT (DESIGN YOUR CIRCULAR PROGRESS HERE)
    def set_value(self, value):
        self.value = value
        self.repaint()
    
    def paintEvent(self, e):
        # Ensure width and height are the same to keep it circular
        size = min(self.width, self.height)
        width = int(size - self.progress_width)
        height = int(size - self.progress_width)
        margin = int(self.progress_width / 2)
        value = int(self.value * 360 / self.max_value)

        # PAINTER
        paint = QPainter()
        paint.begin(self)
        paint.setRenderHint(QPainter.Antialiasing)  # remove pixelated edges
        font = QFont(self.font_family, self.font_size, QFont.Bold)  # Set font to bold
        paint.setFont(font)

        # CREATE RECTANGLE
        rect = QRect(0, 0, size, size)
        paint.setPen(Qt.NoPen)
        paint.drawRect(rect)

        # PEN
        pen = QPen()
        pen.setColor(QColor(self.progress_color))
        pen.setWidth(self.progress_width)
        # Set Round Cap
        if self.progress_rounded_cap:
            pen.setCapStyle(Qt.RoundCap)

        # CREATE ARC / CIRCULAR PROGRESS
        paint.setPen(pen)
        paint.drawArc(margin, margin, width, height, -90 * 16, -value * 16)

        # Draw the image in the center
        image_size = min(width, height) - self.progress_width * 2
        image_rect = QRect(margin + (width - image_size) // 2, margin + (height - image_size) // 2, image_size, image_size)
        paint.drawImage(image_rect, self.image)

        # CREATE TEXT
        pen.setColor(QColor(self.text_color))
        paint.setPen(pen)
        text_rect = QRect(margin, margin, width, height)
        paint.drawText(text_rect, Qt.AlignCenter | Qt.AlignTop, f"{self.value} {self.suffix}")

        # END
        paint.end()
