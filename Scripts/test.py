from config import insert_app_info, insert_app_hourly_info
from datetime import datetime
import time
import pygetwindow as gw
import config
from pywinauto import Application
from serial_id import get_serial_number
from pywinauto.findwindows import ElementNotFoundError
from mysql.connector import OperationalError

tlds = [
    # Generic Top-Level Domains (gTLDs)
    ".com",
    ".org",
    ".net",
    ".biz",
    ".info",
    ".name",
    ".pro",
    ".gov",
    ".edu",
    ".mil",
    # Country Code Top-Level Domains (ccTLDs)
    ".us",
    ".uk",
    ".de",
    ".jp",
    ".cn",
    ".in",
    ".br",
    ".au",
    ".ca",
    ".mx",
    ".fr",
    ".it",
    ".nl",
    ".ru",
    ".np",
    # Newer and Specialized TLDs
    ".co",
    ".io",
    ".ai",
    ".me",
    ".tv",
    ".xyz",
    # Others
    ".jobs",
    ".travel",
    ".mobi",
    ".coop",
]


def get_used_time(start, end):
    time_format = "%H:%M:%S"  # Define the time format as a string
    time_obj1 = datetime.strptime(start, time_format)
    time_obj2 = datetime.strptime(end, time_format)
    time_difference = time_obj2 - time_obj1
    return int(time_difference.total_seconds())  # Convert to integer (seconds)


def extract_url(url):
    if "www." in url:
        url = url.split("www.")[-1]
    if "https://" in url:
        url = url.split("https://")[-1]
    url = tld_checker(url)
    while "." in url:
        url = tld_checker(url)
    return url


def tld_checker(url):
    for tld in tlds:
        if tld in url:
            url = url.split(tld)[0]
            return url
    else:
        url = url.split(".")
        return max(url, key=len)


def google_chr():
    app = Application(backend="uia")
    app.connect(title_re=".*Chrome.*", found_index=0)
    element_name = "Address and search bar"
    dlg = app.top_window()
    try:
        url = dlg.child_window(title=element_name, control_type="Edit").get_value()
        return extract_url(url)
    except ElementNotFoundError:
        time.sleep(3)
        return "chrome"
    except Exception as e:
        print(f"error in the module for chrome \n error is:\n{e}")
        return "chrome"


def get_edge_url():
    while True:
        app = Application(backend="uia")
        app.connect(title_re=".*Microsoft​ Edge.*", found_index=0)
        dlg = app.top_window()
        wrapper = dlg.child_window(title="App bar", control_type="ToolBar")
        try:
            url = wrapper.descendants(control_type="Edit")[0]
            url = url.get_value()
            return extract_url(url)
        except ElementNotFoundError:
            time.sleep(3)
            return "Edge"
        except Exception as e:
            print(f"error in edge module \n{e}")
            return "Edge"


def get_brave_url():
    try:
        app = Application(backend="uia").connect(title_re=".*Brave.*", found_index=0)
        dlg = app.top_window()
        edit_controls = dlg.descendants(control_type="Edit")
        for edit in edit_controls:
            try:
                url_content = edit.get_value()
                if url_content is not None:
                    return extract_url(url_content)
            except Exception as inner_e:
                print(
                    f"Inner error retrieving content from edit control: in brave {inner_e}"
                )
        print("No content found in available Edit controls. in brave")

        return "Brave"
    except ElementNotFoundError:
        time.sleep(3)
        return "Brave"
    except Exception as e:
        print(f"Error retrieving Brave content:\n{e}")
        return "Brave"


def get_fire_fox():
    try:
        app = Application(backend="uia").connect(title_re=".*Firefox.*", found_index=0)
        dlg = app.top_window()
        edit_controls = dlg.descendants(control_type="Edit")
        for edit in edit_controls:
            try:
                url_content = edit.get_value()
                if url_content is not None:
                    return extract_url(url_content)
            except Exception as inner_e:
                print(
                    f"Inner error retrieving content from edit control: in mozila fire fox {inner_e}"
                )
                pass
        # If no content is found in any Edit controls
        print("No content found in available Edit controls.")
        return "Fire Fox"
    except ElementNotFoundError:
        time.sleep(3)
        return "Fire Fox"
    except Exception as e:
        print(f"Error retrieving Firefox content:\n{e}")
        return "Fire Fox"


def track_application() -> list[str, int]:
    """Docstring for track_application"""
    title = None
    active_window = gw.getActiveWindow()

    if active_window is not None:
        if "Google Chrome" in active_window.title:
            title = google_chr()

            time.sleep(1)
        elif "Microsoft​ Edge" in active_window.title:
            title = get_edge_url()

            time.sleep(1)

        elif "Mozilla Firefox" in active_window.title:
            title = get_fire_fox()

            time.sleep(1)

        elif "Brave" in active_window.title:
            title = get_brave_url()

            time.sleep(1)

        else:
            active_window = str(active_window.title).split("-")[-1]
            title = active_window

            time.sleep(1)

    try:
        if title:
            return title
    except (RuntimeError, RuntimeWarning) as e:
        print(f"runtime error as : {e}")
        time.sleep(5)
        return "Error"
    except Exception as e:
        print(e)
        return "Error"
    return "Empty"


prev_window, start_time, end_time = None, None, None


while True:
    try:
        status, name, email = config.get_login_status()
    except (RuntimeError, RuntimeWarning, OperationalError, Exception) as e:
        print(f"could not get login_status {e}")
        time.sleep(5)
        status = None

    if status:
        try:
            title = track_application()
        except (RuntimeError, RuntimeWarning, OperationalError, Exception) as e:
            print(f"could not track application {e}")
            time.sleep(5)
            title = None

        if prev_window is None:
            prev_window = title
        if start_time is None:
            start_time = datetime.now().strftime("%H:%M:%S")

        print("title:", title)

        if (title) and (title != prev_window):
            sereial_id = get_serial_number()
            end_time = datetime.now().strftime("%H:%M:%S")
            used_time = get_used_time(start_time, end_time)
            insert_app_info(prev_window, used_time, email, sereial_id)
            print(f"inserted {prev_window} for time {used_time}")
            
            insert_app_hourly_info(
                start_time, end_time, used_time, prev_window, sereial_id, email
            )
            print(f"updated {prev_window} in hourly table also")
            
            start_time = end_time
            end_time = None
            prev_window = title
        else:
            print(f"still running {title} or {prev_window}")
            pass
    else:
        print("no status")
        time.sleep(10)
