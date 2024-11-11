import win32api,sys
import win32con
import win32gui
import time
import mysql.connector
import datetime
from config import get_connection
import logging

LOG_FILE = r"C:\Users\pande\OneDrive\Pictures\system_events.log"

# Set up logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def insert_Xtra_info(status: bool) -> None:
    """Inserts user's pickup and drop-off details."""
    conn = None
    dbcursor = None

    now = datetime.datetime.now()
    present_date = str(now.today()).split()[0]
    present_day = now.strftime("%A")
    current_time = now.strftime("%I:%M %p")

    try:
        conn = get_connection()
        dbcursor = conn.cursor()

        insert_query = "INSERT INTO info (date, status, time) VALUES (%s, %s, %s)"
        values = (present_date, int(status), current_time)

        dbcursor.execute(insert_query, values)
        conn.commit()

    except Exception as e:
        logging.error(f"Could not insert pickup and drop-off details: {e}")

    finally:
        if dbcursor is not None:
            dbcursor.close()
        if conn is not None:
            conn.close()


def log_event(event):
    """Logs the event with a timestamp to a file."""
    logging.info(event)


def on_system_event(hwnd, msg, wparam, lparam):
    if msg == win32con.WM_POWERBROADCAST:
        if wparam == win32con.PBT_APMSUSPEND:
            insert_Xtra_info(False) # System going to sleep
        elif wparam == win32con.PBT_APMQUERYSUSPEND:
            insert_Xtra_info(False) # System going to hibernate
        elif wparam == win32con.PBT_APMRESUMEAUTOMATIC:
            insert_Xtra_info(True)  # System waking up
    elif msg == win32con.WM_QUERYENDSESSION:
        return True  # Allow the shutdown to proceed
    elif msg == win32con.WM_ENDSESSION:
        if wparam:  # Shutdown is happening
            insert_Xtra_info(False)
            log_event("System shutdown")
        else:  # User logging off
            insert_Xtra_info(False)
            log_event("User logging off")
        sys.exit(0)

    return True


def handle_messages():
    message_map = {
        win32con.WM_POWERBROADCAST: on_system_event,
        win32con.WM_QUERYENDSESSION: on_system_event,
        win32con.WM_ENDSESSION: on_system_event,
    }

    wc = win32gui.WNDCLASS()
    wc.lpfnWndProc = message_map
    wc.hInstance = win32api.GetModuleHandle(None)
    wc.lpszClassName = "MyWindowClass"
    wc_atom = win32gui.RegisterClass(wc)
    hwnd = win32gui.CreateWindow(
        wc_atom, "MyWindow", 0, 0, 0, 0, 0, 0, 0, wc.hInstance, None
    )

    # Log the system startup time
    log_event("System startup")
    insert_Xtra_info(True)

    # Main message loop
    win32gui.PumpMessages()


handle_messages()
