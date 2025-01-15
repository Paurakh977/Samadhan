import sys
from PyQt5 import QtWidgets
from stack_bar import StackedBarGraph,data
from horizontal_progress_bar import CustomProgressBar
from display import App

class Myclass(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200,200,800,800)
        self.setWindowTitle("XyZ")
        self.setupUI()
        
        
    def setupUI(self):
        
        self.central_widget=QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget_layout=QtWidgets.QHBoxLayout(self.central_widget)

        self.frame_1=QtWidgets.QFrame(self.central_widget)
        self.frame_2=QtWidgets.QFrame(self.central_widget)
        self.frame_1_layout=QtWidgets.QGridLayout(self.frame_1)
        self.frame_2_layout=QtWidgets.QGridLayout(self.frame_2)
        
        self.central_widget_layout.addWidget(self.frame_1)
        self.central_widget_layout.addWidget(self.frame_2)
        
        
        self.my_stack=StackedBarGraph(self.frame_2)
        self.my_stack.plotGraph(data)
        self.frame_2_layout.addWidget(self.my_stack)
        
        self.my_bar_frame=QtWidgets.QFrame(self.frame_1)
        self.my_apps_frame=QtWidgets.QFrame(self.frame_1)
        
        self.my_bar_frame.setStyleSheet(" background-color: white")
        self.my_apps_frame.setStyleSheet(" background-color: white")
        
        self.my_bar_frame_layout=QtWidgets.QHBoxLayout(self.my_bar_frame)
        self.my_apps_frame_layout=QtWidgets.QHBoxLayout(self.my_apps_frame)
        
        self.frame_1_layout.addWidget(self.my_bar_frame)
        self.frame_1_layout.addWidget(self.my_apps_frame)
        
        self.Mybar=CustomProgressBar(0.4,0.3,0.2,0.1)
        self.my_bar_frame_layout.addWidget(self.Mybar)
        
        self.myapps=App()
        self.my_apps_frame_layout.addWidget(self.myapps)
        
        
        
def main():
    app=QtWidgets.QApplication(sys.argv)
    win=Myclass()
    win.show()
    sys.exit(app.exec())

if __name__=="__main__":
    main()
    