import sys
import config  # Assuming you're using your database connection
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QListWidget, QListWidgetItem, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

class AppUsageWidget(QWidget):
    def __init__(self, app_name, used_time, icon_path=None):
        super().__init__()
        
        # Create layout for the custom widget (horizontal layout)
        layout = QHBoxLayout()
        
        # App Icon (if provided)
        if icon_path:
            app_icon = QLabel(self)
            app_icon.setPixmap(QIcon(icon_path).pixmap(32, 32))  # Set icon size to 32x32
            layout.addWidget(app_icon)
        
        # App Name
        app_name_label = QLabel(app_name)
        app_name_label.setFont(QFont("Arial", 12))
        layout.addWidget(app_name_label)
        
        # Spacer to push the time to the right
        layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # App Usage Time
        usage_time_label = QLabel(used_time)
        usage_time_label.setFont(QFont("Arial", 12))
        layout.addWidget(usage_time_label)
        
        # Set layout to the custom widget
        self.setLayout(layout)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'App Usage Information'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 400, 300)

        # Create layout
        layout = QVBoxLayout()

        # List widget to display data
        self.list_widget = QListWidget(self)
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

        # Automatically fetch data when the UI opens
        self.fetch_data()

    def format_time(self, minutes):
        """Helper method to format time from minutes to hours and minutes (e.g., 1 h 30 m)."""
        hours = int(minutes // 60)
        mins = int(minutes % 60)
        if hours > 0:
            return f"{hours} h {mins} m"
        return f"{mins} m"

    def fetch_data(self):
        # Clear the list before fetching new data
        self.list_widget.clear()

        try:
            # Database connection
            con = config.get_connection()
            cur = con.cursor()

            # SQL Query
            query = "SELECT * FROM app_usage_info WHERE serial_id = %s ORDER BY tab_name"
            user_serial_id = '1bcfadd1-06b5-4086-b4e9-a5ae90da5af5'

            # Execute the query
            cur.execute(query, (user_serial_id,))
            results = cur.fetchall()

            # Loop through results and add each to the list
            for result in results:
                tab_name = result[0]  # Assuming tab_name is at index 0
                used_time_in_minutes = result[1] / 60  # Convert seconds to minutes
                
                # Format the usage time to hours and minutes
                used_time = self.format_time(used_time_in_minutes)
                
                # Create the custom widget with app name, time, and optional icon
                app_item = QListWidgetItem(self.list_widget)
                custom_widget = AppUsageWidget(tab_name, used_time, icon_path=r'C:\Users\LENOVO\Desktop\pyqt\Samadhan\Images\fb (1).png')  # Replace None with the path to app icons if available
                app_item.setSizeHint(custom_widget.sizeHint())  # Ensure correct sizing of the widget
                
                # Add the custom widget to the list
                self.list_widget.setItemWidget(app_item, custom_widget)

            cur.close()
            con.close()
        except Exception as e:
            error_item = QListWidgetItem(f"Error: {str(e)}")
            self.list_widget.addItem(error_item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
