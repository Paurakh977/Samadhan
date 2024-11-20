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
        total_social_networking = np.sum(social_networking)
        total_entertainment = np.sum(entertainment)
        total_productivity = np.sum(productivity)

        # Define multiple shades of blue and orange
        blue_shades = ["#1E88E5", "#42A5F5", "#90CAF9"]
        orange_shades = ["#FB8C00", "#FFA726", "#FFCC80"]
        gray_shades = ["#C0C0C0", "#D3D3D3", "#E0E0E0"]

        ax = self.canvas.figure.add_subplot(111)
        ax.clear()

        bar_width = 0.5
        max_stack_height = np.max(social_networking + entertainment + productivity)
        padding=0.5 * max_stack_height
        # Stack bars with gradient colors
        p1 = ax.bar(
            times,
            social_networking,
            bar_width,
            label="Social Networking",
            color=blue_shades[0],
        )
        p2 = ax.bar(
            times,
            entertainment,
            bar_width,
            bottom=social_networking,
            label="Entertainment",
            color=orange_shades[0],
        )
        p3 = ax.bar(
            times,
            productivity,
            bar_width,
            bottom=social_networking + entertainment,
            label="Productivity",
            color=gray_shades[0],
        )

        # Add gradient effect
        for i in range(1, 3):
            ax.bar(
                times,
                social_networking / 3,
                bar_width,
                bottom=social_networking * i / 3,
                color=blue_shades[i],
            )
            ax.bar(
                times,
                entertainment / 3,
                bar_width,
                bottom=social_networking + entertainment * i / 3,
                color=orange_shades[i],
            )
            ax.bar(
                times,
                productivity / 3,
                bar_width,
                bottom=social_networking + entertainment + productivity * i / 3,
                color=gray_shades[i],
            )

        ax.text(
            25, max_stack_height + 30,  # Position near the first bar and above the graph
            f"Social Networking: {total_social_networking}m",
            color=blue_shades[0],
            fontsize=16,
            fontweight="bold",
            ha="right",
        )
        ax.text(
            25, max_stack_height + 27,  # Adjust Y position for spacing
            f"Entertainment: {total_entertainment}m",
            color=orange_shades[0],
            fontsize=16,
            fontweight="bold",
            ha="right",
        )
        ax.text(
            25, max_stack_height + 24,  # Adjust Y position for spacing
            f"Productivity: {total_productivity}m",
            color=gray_shades[0],
            fontsize=16,
            fontweight="bold",
            ha="right", 
        )
        
        max_stack_height = np.max(social_networking + entertainment + productivity)
        padding=1 * max_stack_height
        ax.set_yticks([0, 15, 30, 45, 60])
        ax.set_yticklabels(["0m", "15m", "30m", "45m", "60m"], fontsize=10)
        ax.set_ylim(0, max_stack_height + padding)  # Use the updated ylim

        ax.yaxis.set_label_position('left')
        ax.yaxis.tick_left()
        
        ax.set_ylim(0, max_stack_height + 25) 
        ax.set_xlabel("Time of Day", fontsize=12, weight="bold", color="#333333")
        ax.set_title("Daily Screen Time", fontsize=18, weight="bold", color="#333333",loc='center')

        # Remove grid and spines
        ax.grid(False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_visible(False)

        ax.set_xticks(times)
        ax.set_xticklabels(
            [f"{i}h" for i in range(24)],
            rotation=0,
            fontsize=10,
            weight="bold",
            color="gray",
        )
        


        # Add legend outside the plot
        ax.legend(
            loc="upper center", bbox_to_anchor=(0.5, -0.09), ncol=3, frameon=False
        )

        self.canvas.draw()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Digital Wellbeing Graph")
        self.setGeometry(100, 100, 900, 600)

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        self.central_layout = QtWidgets.QVBoxLayout(self.central_widget)

        self.graph = StackedBarGraph(self)
        self.central_layout.addWidget(self.graph)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
