import sys
from PyQt5 import QtWidgets

class AOne(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(800,800,500,500)
        self.setWindowTitle("Page A")
        self.setup_UI()
        
    def setup_UI(self):
        self.centralwidget=QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.central_layout=QtWidgets.QHBoxLayout(self.centralwidget)
        self.centralwidget.setStyleSheet(" background-color: lightpink")
        
        self.frame_1=QtWidgets.QFrame(self.centralwidget)
        self.frame_2=QtWidgets.QFrame(self.centralwidget)
        self.pbtn=QtWidgets.QPushButton("Go to B",self.centralwidget)
        
        self.central_layout.addWidget(self.frame_1)
        self.central_layout.addWidget(self.frame_2)
        self.central_layout.addWidget(self.pbtn)
        
        
        self.frame_1.setStyleSheet("QFrame { background-color: red; border: 1px solid #000; }")
        self.frame_2.setStyleSheet("QFrame { background-color: blue; border: 1px solid #000; }")
        
        self.label1=QtWidgets.QLabel(self.frame_1)
        self.label1.setText("THIS IS FRAME 1 OF PAGE A")
        self.btn1=QtWidgets.QPushButton("BTN1 OF A",self.frame_1)
        self.btn2=QtWidgets.QPushButton("BTN2 OF A",self.frame_1)
        
        self.frame_1_layout=QtWidgets.QVBoxLayout(self.frame_1)
        self.frame_1_layout.addWidget(self.label1)
        self.frame_1_layout.addWidget(self.btn1)
        self.frame_1_layout.addWidget(self.btn2)
        
        self.label_1=QtWidgets.QLabel(self.frame_2)
        self.label_1.setText("THIS IS FRAME 2 OF PAGE A")
        self.btn_1=QtWidgets.QPushButton("BTN OF A",self.frame_2)
        self.btn_2=QtWidgets.QPushButton("BTN2 OF A",self.frame_2)
        
        self.frame_2_layout=QtWidgets.QVBoxLayout(self.frame_2)
        self.frame_2_layout.addWidget(self.label_1)
        self.frame_2_layout.addWidget(self.btn_1)
        self.frame_2_layout.addWidget(self.btn_2)
        
        self.label1.setStyleSheet("color:white;\n font-size:40px;")
        self.label_1.setStyleSheet("color:white;\n font-size:40px;")


def main():
    app=QtWidgets.QApplication(sys.argv)
    win=AOne()
    win.show()
    sys.exit(app.exec())
    
if __name__=="__main__":
    main()
