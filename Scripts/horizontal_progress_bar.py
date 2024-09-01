import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class CustomProgressBar(QWidget):
    def __init__(self, stack1, stack2, stack3, stack4):
        super().__init__()

        # Normalize and adjust the stack percentages
        total = stack1 + stack2 + stack3 + stack4
        self.stack1 = stack1 / total * 100
        self.stack2 = stack2 / total * 100
        self.stack3 = stack3 / total * 100
        self.stack4 = stack4 / total * 100

        self.initUI()

    def initUI(self):
        # Set up the layout
        layout = QVBoxLayout()

        # Add the label above the progress bar with custom font
        label = QLabel('3 h 52 m less than yesterday')
        label.setFont(QFont("Arial", 12, QFont.Bold))
        label.setStyleSheet("color: #444444;")
        layout.addWidget(label)

        # Create a custom progress bar
        self.progressBar = QProgressBar(self)
        self.progressBar.setTextVisible(False)
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(100)  # Set to 100% since we are controlling the chunks manually

        # Customize the appearance with stylesheets
        self.progressBar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid #B0BEC5;
                border-radius: 10px;
                background-color: #ECEFF1;
                height: 20px;
                margin: 5px 0;
            }}
            QProgressBar::chunk {{
                border-radius: 10px;
                background: qlineargradient(
                    spread:pad, 
                    x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {self._hex_color("#67D7C9", self.stack1)}, 
                    stop:{self.stack1/100:.2f} {self._hex_color("#2E4A87", self.stack2)}, 
                    stop:{(self.stack1 + self.stack2)/100:.2f} {self._hex_color("#C48CE2", self.stack3)}, 
                    stop:{(self.stack1 + self.stack2 + self.stack3)/100:.2f} {self._hex_color("#d3d3d3", self.stack4)}
                );
                padding: 2px;
                background-clip: padding;
            }}
        """)

        layout.addWidget(self.progressBar)
        layout.setAlignment(Qt.AlignTop)

        # Set the layout to the widget
        self.setLayout(layout)
        self.setWindowTitle('Stacked Custom Progress Bar')
        self.setGeometry(300, 300, 300, 100)
        self.show()

    def _hex_color(self, color, percentage):
        """
        Adjusts the color based on the given percentage.
        For simplicity, the function returns the original color.
        """
        # The color can be adjusted based on percentage if needed.
        return color

def main():
    # Example user inputs for the four stacks
    stack1 = 0.4  # 40%
    stack2 = 0.2  # 20%
    stack3 = 0.2  # 20%
    stack4 = 0.2  # 20%

    # Ensure the inputs are between 0 and 1 and sum to 1 (or 100%)
    total = stack1 + stack2 + stack3 + stack4
    
    app = QApplication(sys.argv)
    ex = CustomProgressBar(stack1, stack2, stack3, stack4)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
