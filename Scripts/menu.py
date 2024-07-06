from PyQt5 import QtWidgets
import sys,os,A,B,weekly,daily,home,calandar,info
from PyQt5.uic import loadUi

class MenuWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        this_file_location=os.path.dirname(__file__)
        ui_file_location= os.path.abspath(os.path.join(this_file_location,"..","UI","menu_ui.ui"))
        loadUi(ui_file_location,self)
        self.setupUI()    
        
    def setupUI(self):
        self.setWindowTitle("SAMADHAN")
        self.setGeometry(400,100,1400,900)
        
        #findingchild
        self.icon_name_widget=self.findChild(QtWidgets.QWidget,"icon_name_widget")
        self.stackWidget=self.findChild(QtWidgets.QStackedWidget,"stackedWidget")
        self.home_2=self.findChild(QtWidgets.QPushButton,"home_2")
        self.home_1=self.findChild(QtWidgets.QPushButton,"home_1")
        
        
        self.icon_name_widget.setHidden(True)
        
        #clearing stackwidget that were used during making this using qtdesginer
        while self.stackWidget.count() > 0:
            widget = self.stackWidget.widget(0)
            self.stackWidget.removeWidget(widget)
            
       #setting up the windows class
        self.homeWindow=home.HomeWindow()
        self.dailyWindow=daily.DailyWindow()
        self.weeklyWindow=weekly.WeeklyWindow()
        self.calandarWindow=calandar.CalanadarWindow()
        self.infoWindow=info.InfoWindow()
        
    #<------------ NOTE THIS IS FOR TESTING ONLY--------------->    
    
        self.AWindow=A.AOne()
        self.Bwindow=B.BTwo()
        self.stackWidget.addWidget(self.AWindow)
        self.stackWidget.addWidget(self.Bwindow)
        
        self.AWindow.pbtn.clicked.connect(self.get_b)
        self.Bwindow.pbtn.clicked.connect(self.get_a)
    # <-------------NOTE DUMMY ENDS HERE-------------------->  
    
        self.stackWidget.addWidget(self.homeWindow)
        self.stackWidget.addWidget(self.dailyWindow)
        self.stackWidget.addWidget(self.weeklyWindow)
        self.stackWidget.addWidget(self.infoWindow)
        self.stackWidget.addWidget(self.calandarWindow)  
          
        
    def get_a(self):
        self.stackWidget.setCurrentWidget(self.AWindow)
    
    def get_b(self):
        self.stackWidget.setCurrentWidget(self.Bwindow)
        
    
def main():
    app=QtWidgets.QApplication(sys.argv)
    win=MenuWindow()
    sys.exit(app.exec_())
    
if __name__=="__main__":
    main()
    