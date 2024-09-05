import win32api
import win32con
import win32gui
import time
import sys

LOG_FILE = "system_events.log"

def log_event(event):
    """Logs the event with a timestamp to a file."""
    with open(LOG_FILE, "a") as file:
        current_time = time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime())
        file.write(f"{current_time} - {event}\n")

def handler(ctrl_type):
    """Handles console control events."""
    if ctrl_type in [win32con.CTRL_CLOSE_EVENT, win32con.CTRL_LOGOFF_EVENT, win32con.CTRL_SHUTDOWN_EVENT]:
        # log_event("System is shutting down 3")
        sys.exit(0)  # Exit the script

    return True

def on_system_event(hwnd, msg, wparam, lparam):
    
    if msg == win32con.WM_POWERBROADCAST:
        if wparam == win32con.PBT_APMSUSPEND:
            log_event("System is going to sleep")
        elif wparam == win32con.PBT_APMQUERYSUSPEND:
            log_event("System is hibernating")
        elif wparam == win32con.PBT_APMRESUMEAUTOMATIC:
            log_event("System is resuming from sleep or hibernation")
    elif msg == win32con.WM_QUERYENDSESSION:
        # log_event("System shutdown initiated")
        return True  # Allow the shutdown to proceed
    elif msg == win32con.WM_ENDSESSION:
        if wparam:  # Shutdown is happening
            log_event("System is shutting down 1")
        else:  # Session end without shutdown (e.g., log off)
            log_event("User is logging off")
        sys.exit(0)  # Exit the script
    
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
    hwnd = win32gui.CreateWindow(wc_atom, "MyWindow", 0, 0, 0, 0, 0, 0, 0, wc.hInstance, None)

    # Log the system startup time
    log_event("System started")

    # Set console control handler for shutdown
    win32api.SetConsoleCtrlHandler(handler, True)

    try:
        while True:
            win32gui.PumpWaitingMessages()
    except KeyboardInterrupt:
        log_event("System is shutting down 2")

handle_messages()
