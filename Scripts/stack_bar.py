import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class StackedBarGraph(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(StackedBarGraph, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QtWidgets.QVBoxLayout(self)
        self.canvas = FigureCanvas(plt.figure(figsize=(10, 6)))
        self.layout.addWidget(self.canvas)

        self.plotGraph()

    def plotGraph(self):
        times = np.arange(24)  # 24 hours
        social_networking = np.random.randint(5, 15, size=24)
        entertainment = np.random.randint(5, 15, size=24)
        productivity = np.random.randint(5, 15, size=24)

        # Define multiple shades of blue and orange
        blue_shades = ['#1E88E5', '#42A5F5', '#90CAF9']
        orange_shades = ['#FB8C00', '#FFA726', '#FFCC80']
        gray_shades = ['#C0C0C0', '#D3D3D3', '#E0E0E0']

        ax = self.canvas.figure.add_subplot(111)
        ax.clear()

        bar_width = 0.5

        # Stack bars with gradient colors
        p1 = ax.bar(times, social_networking, bar_width, label='Social Networking', color=blue_shades[0])
        p2 = ax.bar(times, entertainment, bar_width, bottom=social_networking, label='Entertainment', color=orange_shades[0])
        p3 = ax.bar(times, productivity, bar_width, bottom=social_networking + entertainment, label='Productivity', color=gray_shades[0])

        # Add gradient effect
        for i in range(1, 3):
            ax.bar(times, social_networking/3, bar_width, bottom=social_networking*i/3, color=blue_shades[i])
            ax.bar(times, entertainment/3, bar_width, bottom=social_networking + entertainment*i/3, color=orange_shades[i])
            ax.bar(times, productivity/3, bar_width, bottom=social_networking + entertainment + productivity*i/3, color=gray_shades[i])

        ax.set_xlabel('Time of Day', fontsize=12, weight='bold', color='#333333')
        ax.set_ylabel('Hours', fontsize=12, weight='bold', color='#333333')
        ax.set_title('Daily Screen Time', fontsize=18, weight='bold', color='#333333')

        # Remove grid and spines
        ax.grid(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        ax.set_xticks(times)
        ax.set_xticklabels([f'{i}h' for i in range(24)], rotation=0, fontsize=10, weight='bold', color='gray')
        ax.set_yticks([])

        # Hide y-axis
        ax.get_yaxis().set_visible(False)

        # Add legend outside the plot
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3, frameon=False)

        self.canvas.draw()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Digital Wellbeing Graph")
        self.setGeometry(100, 100, 900, 600)

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QtWidgets.QVBoxLayout(self.central_widget)

        self.graph = StackedBarGraph(self)
        self.layout.addWidget(self.graph)

        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())