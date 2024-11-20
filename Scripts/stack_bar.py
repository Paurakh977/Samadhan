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
        other = np.random.randint(5, 15, size=24)

        total_social_networking = np.sum(social_networking)
        total_entertainment = np.sum(entertainment)
        total_productivity = np.sum(productivity)
        total_other = np.sum(other)

        # Define color shades
        blue_shades = ["#1E88E5", "#42A5F5", "#90CAF9"]  # Blue for social
        light_blue_shades = ["#63A9F5", "#85C2F7", "#B2D9FB"]  # Refined light blue for entertainment
        orange_shades = ["#FB8C00", "#FFA726", "#FFCC80"]  # Orange for productivity
        gray_shades =  ["#C0C0C0", "#D3D3D3", "#E0E0E0"]  
        
        ax = self.canvas.figure.add_subplot(111)
        ax.clear()

        bar_width = 0.5
        max_stack_height = np.max(social_networking + entertainment + productivity + other)
        padding = 0.5 * max_stack_height

        # Stack bars with the specified colors
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
            color=light_blue_shades[0],
        )
        p3 = ax.bar(
            times,
            productivity,
            bar_width,
            bottom=social_networking + entertainment,
            label="Productivity",
            color=orange_shades[0],
        )
        p4 = ax.bar(
            times,
            other,
            bar_width,
            bottom=social_networking + entertainment + productivity,
            label="Other",
            color=gray_shades[0],
        )

        # Add gradient effect for each category
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
                color=light_blue_shades[i],
            )
            ax.bar(
                times,
                productivity / 3,
                bar_width,
                bottom=social_networking + entertainment + productivity * i / 3,
                color=orange_shades[i],
            )
            ax.bar(
                times,
                other / 3,
                bar_width,
                bottom=social_networking + entertainment + productivity + other * i / 3,
                color=gray_shades[i],
            )

        # Add text annotations for totals
        ax.text(
            25,
            max_stack_height + 32,
            f"Social Networking: {total_social_networking}m",
            color=blue_shades[0],
            fontsize=16,
            fontweight="bold",
            ha="right",
        )
        ax.text(
            25,
            max_stack_height + 29,
            f"Entertainment: {total_entertainment}m",
            color=light_blue_shades[0],
            fontsize=16,
            fontweight="bold",
            ha="right",
        )
        ax.text(
            25,
            max_stack_height + 26,
            f"Productivity: {total_productivity}m",
            color=orange_shades[0],
            fontsize=16,
            fontweight="bold",
            ha="right",
        )
        ax.text(
            25,
            max_stack_height + 23,
            f"Other: {total_other}m",
            color=gray_shades[0],
            fontsize=16,
            fontweight="bold",
            ha="right",
        )

        # Adjust y-axis limits and labels
        ax.set_yticks([0, 15, 30, 45, 60])
        ax.set_yticklabels(["0m", "15m", "30m", "45m", "60m"], fontsize=12)
        ax.set_ylim(0, max_stack_height + padding)

        ax.yaxis.set_label_position("left")
        ax.yaxis.tick_left()

        ax.set_xlabel("Time of Day", fontsize=12, weight="bold", color="#333333")
        ax.set_title(
            "Daily Screen Time", fontsize=18, weight="bold", color="#333333", loc="center"
        )

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
            loc="upper center", bbox_to_anchor=(0.5, -0.09), ncol=4, frameon=False
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
