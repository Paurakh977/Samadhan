import sys,os,logging
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config import insert_user
import login

class SignupWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        this_file_location=os.path.dirname(__file__)
        ui_file_location=os.path.abspath(os.path.join(this_file_location,"..","UI","signup.ui"))
        
        loadUi(ui_file_location,self)
        self.setupUI()
        
    def setupUI(self):
        self.setGeometry(600,200,600,800)
        self.setWindowTitle("SAMADHAN")
        self.login_window=login.LoginWindow()
        self.already_have_an_account=self.findChild(QtWidgets.QPushButton,"signup_btn")
        self.google_login_btn=self.findChild(QtWidgets.QPushButton,"google_btn")
        self.google_login_btn.clicked.connect(self.signup_with_google)
        
    def signup_with_google(self):
        creds_file = os.path.join(os.path.dirname(__file__),"API", 'credentials.json')
        scopes = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email', 'openid']

        try:
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, scopes)
            creds = flow.run_local_server(port=0)
        except Exception as e:
            logging.error(f"Error during authentication: {e}")
            return

        try:
            # Use the credentials to build the People API service
            service = build('people', 'v1', credentials=creds)
            profile = service.people().get(resourceName='people/me', personFields='names,emailAddresses').execute()

            # Retrieve the uaser's name and email
            name = profile.get('names', [{}])[0].get('displayName', 'N/A')
            email = profile.get('emailAddresses', [{}])[0].get('value', 'N/A')

            # Update the label with the user's name and email
            insert_user(name, email,'Google')
            print(f'Name: {name}\nEmail: {email}')
        except Exception as e:
            logging.error(f"Error retrieving profile information: {e}")
    
    

def main():
    app=QtWidgets.QApplication(sys.argv)
    win=SignupWindow()
    win.show()
    sys.exit(app.exec_())
    
if __name__=="__main__":
    main()