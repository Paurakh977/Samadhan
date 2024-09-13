# import win32api
# import win32con
# import win32gui
# import time
# import sys
# import mysql.connector
# import datetime

# LOG_FILE = r"C:\Users\pande\OneDrive\Pictures\system_events.log"


# def get_connection():
#     """Establish and return a new database connection."""
#     return mysql.connector.connect(
#         host="localhost", user="root", password="", database="samadhandb"
#     )


# def insert_Xtra_info(status: bool) -> None:
#     """Inserts user's pickup and drop-off details."""
#     conn = None
#     dbcursor = None

#     now = datetime.datetime.now()
#     present_date = str(now.today()).split()[0]
#     present_day = now.strftime("%A")
#     current_time = now.strftime("%I:%M %p")
#     now = datetime.datetime.now()
#     present_date = str(now.today()).split()[0]
#     present_day = now.strftime("%A")
#     current_time = now.strftime("%I:%M %p")

#     try:
#         conn = get_connection()
#         dbcursor = conn.cursor()

#         insert_query = "INSERT INTO info (date, status, time) VALUES (%s, %s, %s)"
#         values = (present_date, int(status), current_time)

#         dbcursor.execute(insert_query, values)
#         conn.commit()

#     except Exception as e:
#         print(f"Error: {e}\nCould not insert pickup and drop-off details")

#     finally:
#         if dbcursor is not None:
#             dbcursor.close()
#         if conn is not None:
#             conn.close()


# def log_event(event):
#     """Logs the event with a timestamp to a file."""
#     with open(LOG_FILE, "a") as file:
#         current_time = time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime())
#         file.write(f"{current_time} - {event}\n")


# def handler(ctrl_type):
#     """Handles console control events."""
#     if ctrl_type in [
#         win32con.CTRL_CLOSE_EVENT,
#         win32con.CTRL_LOGOFF_EVENT,
#         win32con.CTRL_SHUTDOWN_EVENT,
#     ]:
#         # log_event("System is shutting down 3")
#         sys.exit(0)  # Exit the script

#     return True


# def on_system_event(hwnd, msg, wparam, lparam):
#     if msg == win32con.WM_POWERBROADCAST:
#         if wparam == win32con.PBT_APMSUSPEND:
#             insert_Xtra_info(False)
#         elif wparam == win32con.PBT_APMQUERYSUSPEND:
#             insert_Xtra_info(False)
#         elif wparam == win32con.PBT_APMRESUMEAUTOMATIC:
#             insert_Xtra_info(True)
#     elif msg == win32con.WM_QUERYENDSESSION:
#         # log_event("System shutdown initiated")
#         return True  # Allow the shutdown to proceed
#     elif msg == win32con.WM_ENDSESSION:
#         if wparam:  # Shutdown is happening
#             log_event("shutting down")
#             insert_Xtra_info(False)
#         else:  # Session end without shutdown (e.g., log off)
#             insert_Xtra_info("User is logging off")
#         sys.exit(0)  # Exit the script

#     return True


# def handle_messages():
#     message_map = {
#         win32con.WM_POWERBROADCAST: on_system_event,
#         win32con.WM_QUERYENDSESSION: on_system_event,
#         win32con.WM_ENDSESSION: on_system_event,
#     }

#     wc = win32gui.WNDCLASS()
#     wc.lpfnWndProc = message_map
#     wc.hInstance = win32api.GetModuleHandle(None)
#     wc.lpszClassName = "MyWindowClass"
#     wc_atom = win32gui.RegisterClass(wc)
#     hwnd = win32gui.CreateWindow(
#         wc_atom, "MyWindow", 0, 0, 0, 0, 0, 0, 0, wc.hInstance, None
#     )

#     # Log the system startup time
#     log_event("Sys started")
#     insert_Xtra_info(True)

#     # Set console control handler for shutdown
#     win32api.SetConsoleCtrlHandler(handler, True)

#     try:
#         while True:
#             win32gui.PumpWaitingMessages()
#     except KeyboardInterrupt:
#         log_event("System is shutting down 2")


# handle_messages()
