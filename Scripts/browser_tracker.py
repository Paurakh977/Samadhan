import time
import pygetwindow as gw
import config
from pywinauto import Application
import session
import serial_id

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
    except Exception as e:
        print(f"error in the module for chrome \n error is:\n{e}")
        return None


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
        except Exception as e:
            print(f"error in edge module \n{e}")
            return None


def get_fire_fox():
    try:
        app = Application(backend="uia").connect(title_re=".*Mozilla Firefox.*")
        dlg = app.top_window()
        url_bar = dlg.child_window(control_type="Edit", found_index=0)
        url = url_bar.get_value()
        return extract_url(url)
    except Exception as e:
        try:
            url_bar = dlg.descendants(control_type="Edit")[0]
            url = url_bar.get_value()
            return extract_url(url)
        except Exception as nested_e:
            print(f"Error in Firefox module: {nested_e}")
            return None


def main():
    # if session.session_started:
        used_time = 0
        # user_email = session.session_email
        user_email = 'yareyaredazey108@gmail.com'
        while True:
            title = None
            active_window = gw.getActiveWindow()

            if active_window is not None:
                if "Google Chrome" in active_window.title:
                    title = google_chr()
                    used_time += 3
                    time.sleep(3)
                elif "Microsoft​ Edge" in active_window.title:
                    title = get_edge_url()
                    used_time += 3
                    time.sleep(3)

                elif "Mozilla Firefox" in active_window.title:
                    title = get_fire_fox()
                    used_time += 3
                    time.sleep(3)

                else:
                    print("no browser active rn")
                    time.sleep(3)

            if title:
                db = config
                s_id = serial_id.get_serial_number()
                db.insert(title, used_time, user_email, s_id)
                print(f"  {user_email} {s_id} {title}")

main()
