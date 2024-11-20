import sys
from PyQt5 import QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class StackedBarGraph(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(StackedBarGraph, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QtWidgets.QVBoxLayout(self)
        self.canvas = FigureCanvas(plt.figure(figsize=(10, 6)))
        self.layout.addWidget(self.canvas)

    def plotGraph(self, data):
        times = list(range(24))  # Fixed 24-hour range
        social_networking = [data["social_networking"].get(hour, 0) for hour in times]
        entertainment = [data["entertainment"].get(hour, 0) for hour in times]
        productivity = [data["productivity"].get(hour, 0) for hour in times]
        other = [data["other"].get(hour, 0) for hour in times]

        total_social_networking = sum([ i for i in data["social_networking"].values()])
        total_entertainment = sum([ i for i in data["entertainment"].values()])
        total_productivity = sum([ i for i in data["productivity"].values()])
        total_other = sum([ i for i in data["other"].values()])

        
        # Define gradient shades for each category
        blue_shades = ["#1E88E5", "#42A5F5", "#90CAF9"]  # Social Networking
        light_blue_shades = ["#63A9F5", "#85C2F7", "#B2D9FB"]  # Entertainment
        orange_shades = ["#FB8C00", "#FFA726", "#FFCC80"]  # Productivity
        gray_shades = ["#C0C0C0", "#D3D3D3", "#E0E0E0"]  # Other

        ax = self.canvas.figure.add_subplot(111)
        ax.clear()

        bar_width = 0.5
        max_stack_height = 60  # Maximum height is fixed to 60 minutes
        padding = 5  # Padding above the stack for aesthetics

        # Plot bars with gradient shades
        for i in range(3):
            ax.bar(
                times,
                [val / 3 for val in social_networking],
                bar_width,
                bottom=[val * i / 3 for val in social_networking],
                color=blue_shades[i],
            )
            ax.bar(
                times,
                [val / 3 for val in entertainment],
                bar_width,
                bottom=[
                    (social_networking[j] + entertainment[j] * i / 3)
                    for j in range(len(times))
                ],
                color=light_blue_shades[i],
            )
            ax.bar(
                times,
                [val / 3 for val in productivity],
                bar_width,
                bottom=[
                    (social_networking[j] + entertainment[j] + productivity[j] * i / 3)
                    for j in range(len(times))
                ],
                color=orange_shades[i],
            )
            ax.bar(
                times,
                [val / 3 for val in other],
                bar_width,
                bottom=[
                    (
                        social_networking[j]
                        + entertainment[j]
                        + productivity[j]
                        + other[j] * i / 3
                    )
                    for j in range(len(times))
                ],
                color=gray_shades[i],
            )


        ax.text(
            25,
            max_stack_height + 12 ,
            f"Social Networking: {total_social_networking}m",
            color=blue_shades[0],
            fontsize=16,
            fontweight="bold",
            ha="right",
        )
        ax.text(
            25,
            max_stack_height + 9 ,
            f"Entertainment: {total_entertainment}m",
            color=light_blue_shades[0],
            fontsize=16,
            fontweight="bold",
            ha="right",
        )
        ax.text(
            25,
            max_stack_height + 6,
            f"Productivity: {total_productivity}m",
            color=orange_shades[0],
            fontsize=16,
            fontweight="bold",
            ha="right",
        )
        ax.text(
            25,
            max_stack_height + 3,
            f"Other: {total_other}m",
            color=gray_shades[0],
            fontsize=16,
            fontweight="bold",
            ha="right",
        )

        # Adjust y-axis limits and labels
        ax.set_ylim(0, max_stack_height + padding)
        ax.set_yticks(range(0, max_stack_height + 1, 15))  # Adjusted ticks for 15-minute intervals
        ax.set_yticklabels(
            [f"{i}m" for i in range(0, max_stack_height + 1, 15)],
            fontsize=12,
        )

        ax.grid(False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        
        # Add labels and formatting
        ax.set_xlabel("Time of Day", fontsize=12, weight="bold")
        ax.set_title("Daily Screen Time", fontsize=18, weight="bold")
        ax.set_xticks(times)
        ax.set_xticklabels([f"{i}h" for i in times], rotation=0, fontsize=10, weight="bold")
        ax.legend(
            ["Social Networking", "Entertainment", "Productivity", "Other"],
            loc="upper center",
            bbox_to_anchor=(0.5, -0.09),
            ncol=4,
            frameon=False,
        )
        self.canvas.draw()

data = {
            "social_networking": {
                0: 5, 1: 10, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 15, 8: 8, 9: 5,
                10: 0, 11: 5, 12: 2, 13: 25, 14: 3, 15: 10, 0: 6, 17: 10, 18: 8, 19: 10,
                20: 5, 21: 7, 22: 5, 23: 0
            },
            "entertainment": {
                0: 10, 1: 5, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 8, 8: 15, 9: 10,
                10: 0, 11: 0, 12: 10, 0: 5, 14: 17, 15: 12, 7: 10, 17: 15, 18: 2, 19: 5,
                20: 10, 21: 10, 22: 8, 23: 5
            },
            "productivity": {
                0: 15, 1: 8, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 15, 8: 10, 9: 10,
                10: 8, 11: 10, 12: 0, 13: 2, 14: 10, 15: 10, 0: 15, 17: 13, 18: 3, 19: 8,
                20: 15, 21: 10, 22: 12, 23: 10
            },
            "other": {
                0: 30, 1: 30, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 7, 8: 12, 9: 20,
                10: 2, 11: 40, 12: 12, 13: 10, 0: 13, 15: 12, 0: 23, 17: 17, 18: 25, 19: 35,
                20: 30, 21: 28, 22: 35, 23: 45
            }
        }

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Digital Wellbeing Graph")
        self.setGeometry(100, 100, 900, 600)

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        self.central_layout = QtWidgets.QVBoxLayout(self.central_widget)

        # Create the graph widget
        self.graph = StackedBarGraph(self)
        self.central_layout.addWidget(self.graph)
        
        self.graph.plotGraph(data)



        


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
