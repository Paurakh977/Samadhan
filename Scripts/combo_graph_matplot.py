import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class EconomicIndicatorsGraph(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(EconomicIndicatorsGraph, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QtWidgets.QVBoxLayout(self)
        self.canvas = FigureCanvas(plt.figure(figsize=(10, 6)))
        self.layout.addWidget(self.canvas)

        self.plotGraph()

    def plotGraph(self):
        years = np.arange(2066, 2083)
        market_cap = [1200, 1150, 1200, 1500, 2400, 2300, 2000, 2200, 3600, 2800, 2600, 3100, 2700, 3500, 3700, 3400, 3300]
        market_cap_to_gdp_ratio = [20, 22, 24, 28, 35, 32, 30, 33, 60, 55, 58, 62, 68, 70, 72, 75, 78]

        # Create the figure and primary y-axis
        fig = self.canvas.figure
        ax1 = fig.add_subplot(111)
        fig.suptitle("Economic Indicators", fontsize=16, fontweight='bold') 

        # Bar chart for Market Capitalization
        bar_colors = plt.cm.Blues(np.linspace(0.3, 0.9, len(market_cap)))
 

        bars = ax1.bar(years, market_cap, color=bar_colors, alpha=0.7, label='Market Capitalization (in billions)')
        ax1.set_xlabel('Fiscal Year')
        ax1.set_ylabel('Market Capitalization (in billions)', color='green', fontsize=12)
        ax1.tick_params(axis='y', labelcolor='green')
        ax1.spines['left'].set_color('green')
        ax1.grid(True, which='major', axis='y', linestyle='-', alpha=0.6)

        # Add value labels on top of bars
        for bar in bars:
            yval = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2, yval + 50, f"{yval}", ha='center', va='bottom', fontsize=10, color='darkgreen')

        # Secondary y-axis for Market Cap to GDP ratio
        ax2 = ax1.twinx()
        line, = ax2.plot(years, market_cap_to_gdp_ratio, color='dodgerblue', linewidth=2.5, marker='*', markersize=13, label='Market Cap to GDP ratio (%)')
        ax2.set_ylabel('Market Cap to GDP ratio (%)', color='dodgerblue', fontsize=12)
        ax2.tick_params(axis='y', labelcolor='dodgerblue')
        ax2.spines['right'].set_color('dodgerblue')
        ax2.grid(False)

        # Styling line plot markers
        line.set_markerfacecolor('orange')
        line.set_markeredgewidth(1.0)
        line.set_markeredgecolor('black')

        # Hide top and right spines
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)

        # Legends and layout adjustments
        fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.95), fontsize=10, frameon=False)
        self.canvas.draw()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Economic Indicators Graph")
        self.setGeometry(100, 100, 900, 600)

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        self.central_layout = QtWidgets.QVBoxLayout(self.central_widget)

        self.graph = EconomicIndicatorsGraph(self)
        self.central_layout.addWidget(self.graph)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
