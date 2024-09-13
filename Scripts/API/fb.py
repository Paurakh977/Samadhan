import sys, signupp
import webbrowser
import requests
from flask import Flask, request
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
)
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets

app = Flask(__name__)
app.secret_key = "6a0cc1c6ba2bf2304d9f0bc36d825456"  # Your secret key here

# Facebook app details (replace with your actual client ID and secret)
client_id = "1642745376490841"
client_secret = "6a0cc1c6ba2bf2304d9f0bc36d825456"
redirect_uri = "http://localhost:5000/callback"
scope = "email"


# PyQt5 application window
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(600, 200, 600, 800)
        self.setWindowTitle("SAMADHAN")
        loadUi(r"C:\Users\pande\OneDrive\Desktop\PyQt\Samadhan-App\UI\Login.ui", self)

        self.go_to_signup = self.findChild(QtWidgets.QPushButton, "signup_btn")
        self.login_btn = self.findChild(QtWidgets.QAbstractButton, "login_btn")

        self.fb_login_btn = self.findChild(QPushButton, "fb_btn")
        self.fb_login_btn.clicked.connect(self.login_with_facebook)

        self.go_to_signup.clicked.connect(self.get_signup_window)

    def get_signup_window(self):
        signup_window = signupp.SignupWindow()  # Create an instance of SignupWindow
        signup_window.show()  # Show the SignupWindow
        self.close()

    def login_with_facebook(self):
        auth_url = f"https://www.facebook.com/v20.0/dialog/oauth?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"
        webbrowser.open(auth_url)

    def closeEvent(self, event):
        # Shutdown Flask server when closing the window
        shutdown_server()
        event.accept()


# Flask routes
@app.route("/")
def index():
    return "Hello, World!"


@app.route("/callback")
def callback():
    error = request.args.get("error")
    if error:
        return f"Error: {error}"

    code = request.args.get("code")

    # Exchange code for access token
    token_url = "https://graph.facebook.com/v20.0/oauth/access_token"
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
    }

    response = requests.get(token_url, params=params)
    data = response.json()

    access_token = data["access_token"]

    # Get user's name and email
    graph_url = (
        f"https://graph.facebook.com/me?fields=name,email&access_token={access_token}"
    )
    user_response = requests.get(graph_url)
    user_data = user_response.json()

    # Update GUI with user info
    print(f"Hello, {user_data['name']}. Your email is: {user_data['email']}")

    # Shutdown Flask server
    shutdown_server()

    return "Login successful! You can now close this window."


def shutdown_server():
    func = request.environ.get("werkzeug.server.shutdown")
    if func:
        func()


if __name__ == "__main__":
    # Start Flask in a separate thread
    server_thread = QThread()
    server_thread.run = lambda: app.run(debug=False)
    server_thread.start()

    # Start PyQt5 application
    app = QApplication(sys.argv)
    main_window = LoginWindow()
    main_window.show()

    sys.exit(app.exec_())
