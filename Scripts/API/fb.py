import sys
import webbrowser
import requests
from flask import Flask, request, redirect
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel

# Flask application setup
app = Flask(__name__)
app.secret_key = '6a0cc1c6ba2bf2304d9f0bc36d825456'

# Facebook app details
client_id = '1642745376490841'
client_secret = '6a0cc1c6ba2bf2304d9f0bc36d825456'
redirect_uri = 'http://localhost:5000/callback'
scope = 'email'

# PyQt5 application window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Facebook OAuth Login')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel('Click below to login with Facebook')
        layout.addWidget(self.label)

        self.login_button = QPushButton('Login with Facebook')
        self.login_button.clicked.connect(self.login_with_facebook)
        layout.addWidget(self.login_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def login_with_facebook(self):
        auth_url = f'https://www.facebook.com/v20.0/dialog/oauth?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}'
        webbrowser.open(auth_url)

# Flask routes
@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/callback')
def callback():
    error = request.args.get('error')
    if error:
        return f'Error: {error}'

    code = request.args.get('code')

    # Exchange code for access token
    token_url = 'https://graph.facebook.com/v20.0/oauth/access_token'
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri
    }

    response = requests.get(token_url, params=params)
    data = response.json()

    access_token = data['access_token']

    # Get user's name and email
    graph_url = f'https://graph.facebook.com/me?fields=name,email&access_token={access_token}'
    user_response = requests.get(graph_url)
    user_data = user_response.json()

    # Update GUI with user info
    main_window.label.setText(f"Hello, {user_data['name']}. Your email is: {user_data['email']}")

    # Shutdown Flask server
    shutdown_server()

    return 'Login successful! You can now close this window.'

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func:
        func()

if __name__ == '__main__':
    # Start Flask in a separate thread
    from threading import Thread
    Thread(target=app.run, kwargs={'debug': False}).start()

    # Start PyQt5 application
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
