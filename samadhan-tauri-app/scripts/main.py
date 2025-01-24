from datetime import datetime
import time
import pygetwindow as gw
import config
from pywinauto import Application
from serial_id import get_serial_number
from pywinauto.findwindows import ElementNotFoundError
import logging
import re
import threading
from functools import lru_cache


# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


tlds = [
    ".com", ".org", ".net", ".biz", ".info", ".name", ".pro", ".gov", ".edu", ".mil",
    ".us", ".uk", ".de", ".jp", ".cn", ".in", ".br", ".au", ".ca", ".mx", ".fr", ".it",
    ".nl", ".ru", ".np", ".co", ".io", ".ai", ".me", ".tv", ".xyz", ".jobs", ".travel",
    ".mobi", ".coop"
]


class AppTracker:
    def __init__(self):
        self.prev_window = None
        self.start_time = None
        self.end_time = None
        self._serial_id = None
        self._last_url = None
        self._last_window_title = None
        self._tld_pattern = re.compile(r'({})'.format('|'.join(map(re.escape, sorted(tlds, key=len, reverse=True)))))
        self._browser_handlers = {
            "Google Chrome": self.google_chr,
            "Microsoft Edge": self.get_edge_url,
            "Mozilla Firefox": self.get_fire_fox,
            "Brave": self.get_brave_url
        }
        self._url_cache = {}
        self._cache_lock = threading.Lock()
        self._last_active_time = time.time()


    def get_used_time(self, start, end):
        return int((datetime.strptime(end, "%H:%M:%S") -
                  datetime.strptime(start, "%H:%M:%S")).total_seconds())


    def tld_checker(self, url):
        match = self._tld_pattern.search(url)
        if match:
            return url.split(match.group())[0]
        return max(url.split("."), key=len)


    @lru_cache(maxsize=1000)
    def extract_url(self, url: str) -> str:
        """Cached URL extraction"""
        url = re.sub(r'(www\.|https?://)', '', url, count=1, flags=re.IGNORECASE)
        while "." in url:
            new_url = self.tld_checker(url)
            if new_url == url:
                break
            url = new_url
        return url


    def google_chr(self):
        """Original Chrome URL extraction with optimizations"""
        try:
            app = Application(backend="uia").connect(title_re=".*Chrome.*", found_index=0)
            dlg = app.top_window()
            url = dlg.child_window(title="Address and search bar", control_type="Edit").get_value()
            return self.extract_url(url)
        except ElementNotFoundError:
            return "chrome"
        except Exception as e:
            logging.error(f"Chrome error: {str(e)}")
            return "chrome"


    def get_edge_url(self):
        """Edge URL extraction with reduced polling"""
        try:
            app = Application(backend="uia").connect(title_re=".*Microsoft Edge.*", found_index=0)
            dlg = app.top_window()
            wrapper = dlg.child_window(title="App bar", control_type="ToolBar")
            url = wrapper.descendants(control_type="Edit")[0].get_value()
            return self.extract_url(url)
        except (ElementNotFoundError, IndexError):
            return "Edge"
        except Exception as e:
            logging.error(f"Edge error: {str(e)}")
            return "Edge"


    def get_brave_url(self):
        """Brave URL extraction with caching"""
        try:
            app = Application(backend="uia").connect(title_re=".*Brave.*", found_index=0)
            dlg = app.top_window()
            for edit in dlg.descendants(control_type="Edit")[:3]:  # Check first 3 elements
                try:
                    if url := edit.get_value():
                        return self.extract_url(url)
                except Exception:
                    continue
            return "Brave"
        except ElementNotFoundError:
            return "Brave"
        except Exception as e:
            logging.error(f"Brave error: {str(e)}")
            return "Brave"


    def get_fire_fox(self):
        """Firefox URL extraction with optimized element search"""
        try:
            app = Application(backend="uia").connect(title_re=".*Firefox.*", found_index=0)
            dlg = app.top_window()
            for edit in dlg.descendants(control_type="Edit")[:3]:  # Limit search
                try:
                    if url := edit.get_value():
                        return self.extract_url(url)
                except Exception:
                    continue
            return "Firefox"
        except ElementNotFoundError:
            return "Firefox"
        except Exception as e:
            logging.error(f"Firefox error: {str(e)}")
            return "Firefox"


    def track_application(self) -> str:
        """Optimized window tracking with caching"""
        try:
            active_window = gw.getActiveWindow()
            if not active_window:
                return self.prev_window or "Empty"
            
            window_title = active_window.title
            
            # Return cached result if window hasn't changed
            if window_title == self._last_window_title:
                return self.prev_window or "Empty"
            
            self._last_window_title = window_title
            
            # Check browser handlers
            for browser_name, handler in self._browser_handlers.items():
                if browser_name in window_title:
                    result = handler()
                    break
            else:
                result = str(window_title).split("-")[-1].strip()
            
            # Update cache and return
            if result and result != self._last_url:
                self._last_url = result
                return result
            
            return self.prev_window or "Empty"
            
        except Exception as e:
            logging.error(f"Tracking error: {str(e)}")
            return "Error"


    def run(self):
        """Highly optimized main loop with batching"""
        poll_interval = 1.5
        error_sleep = 5
        batch_size = 10  # Process 10 apps at a time
        batch_timeout = 50  # Or process after 50 seconds
        last_batch_time = time.time()
        pending_updates = []
        
        while True:
            try:
                if not config.get_login_status()[0]:
                    time.sleep(10)
                    continue

                title = self.track_application()
                current_time = time.time()

                if not self.prev_window:
                    self.prev_window = title
                    self.start_time = datetime.now().strftime("%H:%M:%S")
                    time.sleep(poll_interval)
                    continue

                if title and title != self.prev_window:
                    self.end_time = datetime.now().strftime("%H:%M:%S")
                    used_time = self.get_used_time(self.start_time, self.end_time)
                    
                    # Add to batch
                    pending_updates.append((
                        self.prev_window, used_time, 
                        config.get_login_status()[2], 
                        get_serial_number()
                    ))
                    print(f"\nAdded to batch: {self.prev_window}")

                    # Process batch if full or timeout reached
                    if len(pending_updates) >= batch_size or \
                       (current_time - last_batch_time) >= batch_timeout:
                        print(f"\nProcessing batch of {len(pending_updates)} apps...")
                        self._process_batch(pending_updates)
                        pending_updates = []
                        last_batch_time = current_time

                    self.start_time = self.end_time
                    self.prev_window = title

                time.sleep(poll_interval)

            except Exception as e:
                logging.error(f"Main loop error: {str(e)}")
                time.sleep(error_sleep)

    def _process_batch(self, updates):
        try:
            with config.get_db_connection() as conn:
                with conn.cursor() as cursor:
                    # First store original data
                    for app_name, used_time, email, serial_id in updates:
                        config.insert_app_info(
                            tab_name=app_name,
                            used_time=used_time,
                            user_email=email,
                            serial_id=serial_id
                        )
                    
                    # Get categorized times
                    logging.info("Getting app categories from Gemini...")
                    category_times = config.categorize_batch_apps(updates)
                    logging.info(f"Category times received: {category_times}")
                    
                    # Store categorized data
                    for category, total_time in category_times.items():
                        logging.info(f"Storing category data: {category} -> {total_time}s")
                        config.insert_app_hourly_info(
                            start_time=self.start_time,
                            end_time=self.end_time,
                            used_time=total_time,
                            app_name=category,
                            serial_id=get_serial_number(),
                            user_email=config.get_login_status()[2]
                        )
                    conn.commit()
        except Exception as e:
            logging.error(f"Batch processing error: {e}")


if __name__ == "__main__":
    tracker = AppTracker()
    tracker.run()



