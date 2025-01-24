import time
import datetime
from mysql.connector import Error, OperationalError, pooling
from functools import lru_cache, wraps
from contextlib import contextmanager
import logging
from typing import Dict, Tuple, List
import threading
import json
import subprocess
import requests
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

# Global connection pool with lock
pool = None
pool_lock = threading.Lock()

# Move to environment variables
API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyD45DzCPVEza4VlQK-i_E8nL_NKUkJgfTA')

# Increase cache size and timeout for frequently accessed data
@lru_cache(maxsize=100, typed=True)
def get_login_status() -> Tuple[bool, str, str]:
    """Cached login status with increased cache size"""
    return True, "dada", "dada@gmail.com"

# Add connection pool retry decorator
def with_retry(max_attempts: int = 3, delay: int = 1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except (OperationalError, Error) as e:
                    if attempt == max_attempts - 1:
                        raise
                    logging.warning(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(delay * (2 ** attempt))  # Exponential backoff
            return None
        return wrapper
    return decorator

@with_retry()
def initialize_pool():
    """Thread-safe pool initialization"""
    global pool
    with pool_lock:
        if pool is not None:
            return

        pool_config = {
            "pool_name": "mypool",
            "pool_size": 10,  # Reduced from 20 to prevent connection issues
            "host": "127.0.0.1",
            "user": "root",
            "password": "",
            "database": "samadhandb",
            "connect_timeout": 10,
            "use_pure": True,
            "autocommit": True,
            "buffered": True
        }
        # Removed unsupported options that were causing errors
        
        try:
            pool = pooling.MySQLConnectionPool(**pool_config)
            logging.info("Database pool initialized successfully")
        except Error as e:
            logging.error(f"Failed to initialize pool: {e}")
            raise

# Optimize the database connection context manager
@contextmanager
def get_db_connection():
    """Enhanced connection manager"""
    connection = None
    try:
        if pool is None:
            initialize_pool()
        connection = pool.get_connection()
        yield connection
    except OperationalError as e:
        logging.error(f"Database operational error: {e}")
        raise
    except Error as e:
        logging.error(f"Database error: {e}")
        raise
    finally:
        if connection:
            try:
                connection.close()
            except Error:
                pass
        
def insert_app_info(tab_name, used_time, user_email, serial_id):
    """App info insertion with proper cursor handling"""
    now = datetime.datetime.now()
    present_date = str(now.date())
    present_day = now.strftime("%A")

    with get_db_connection() as conn:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                """SELECT used_time, used_date FROM app_usage_info 
                   WHERE tab_name=%s AND used_day=%s AND email=%s AND serial_id=%s""",
                (tab_name, present_day, user_email, serial_id)
            )
            row = cursor.fetchone()

            if row:
                if str(row['used_date']) == present_date:
                    new_used_time = int(row['used_time']) + used_time
                    cursor.execute(
                        """UPDATE app_usage_info 
                           SET used_time=%s 
                           WHERE tab_name=%s AND used_day=%s AND email=%s AND serial_id=%s""",
                        (new_used_time, tab_name, present_day, user_email, serial_id)
                    )
                    logging.info(f"Updated {tab_name} usage: {new_used_time}s")
                else:
                    cursor.execute(
                        "DELETE FROM app_usage_info WHERE used_day=%s AND email=%s",
                        (present_day, user_email)
                    )
                    cursor.execute(
                        """INSERT INTO app_usage_info 
                           (tab_name, used_time, email, used_day, used_date, serial_id) 
                           VALUES (%s, %s, %s, %s, %s, %s)""",
                        (tab_name, used_time, user_email, present_day, present_date, serial_id)
                    )
                    logging.info(f"New day: Cleared old data and inserted {tab_name}")
            else:
                cursor.execute(
                    """INSERT INTO app_usage_info 
                       (tab_name, used_time, email, used_day, used_date, serial_id) 
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (tab_name, used_time, user_email, present_day, present_date, serial_id)
                )
                logging.info(f"Inserted new record for {tab_name}")
            conn.commit()

def insert_app_hourly_info(start_time, end_time, used_time, app_name, serial_id, user_email):
    """Insert categorized app data into hourly table with multi-hour support"""
    now = datetime.datetime.now()
    present_date = str(now.date())
    present_day = now.strftime("%A")
    st_hour = start_time.split(":")[0]
    end_hour = end_time.split(":")[0]

    def _update_or_insert_hour(cursor, hour, duration):
        """Helper function to handle single hour update/insert"""
        cursor.execute(
            """SELECT used_time, used_date FROM app_hour_data 
               WHERE app_name=%s AND hour=%s AND used_day=%s AND email=%s AND serial_id=%s""",
            (app_name, hour, present_day, user_email, serial_id)
        )
        row = cursor.fetchone()

        if row:
            if str(row[1]) == present_date:
                # Same day - update existing record
                new_used_time = int(row[0]) + duration
                cursor.execute(
                    """UPDATE app_hour_data 
                       SET used_time=%s 
                       WHERE app_name=%s AND hour=%s AND used_day=%s AND email=%s AND serial_id=%s""",
                    (new_used_time, app_name, hour, present_day, user_email, serial_id)
                )
                logging.info(f"Updated hourly data for {app_name} hour {hour}: {new_used_time}s")
            else:
                # Different day - clear old and insert new
                cursor.execute(
                    "DELETE FROM app_hour_data WHERE used_day=%s AND email=%s",
                    (present_day, user_email)
                )
                cursor.execute(
                    """INSERT INTO app_hour_data 
                       (app_name, hour, used_time, used_day, used_date, email, serial_id)
                       VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (app_name, hour, duration, present_day, present_date, user_email, serial_id)
                )
                logging.info(f"New day: Inserted hourly data for {app_name} hour {hour}")
        else:
            # No existing record - insert new
            cursor.execute(
                """INSERT INTO app_hour_data 
                   (app_name, hour, used_time, used_day, used_date, email, serial_id)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (app_name, hour, duration, present_day, present_date, user_email, serial_id)
            )
            logging.info(f"Inserted new hourly data for {app_name} hour {hour}: {duration}s")

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                if st_hour == end_hour:
                    # Same hour - simple update/insert
                    _update_or_insert_hour(cursor, st_hour, used_time)
                else:
                    # Multiple hours - calculate distribution
                    usage_info = calculate_hourly_usage(start_time, end_time)
                    logging.info(f"Multi-hour distribution: {usage_info}")
                    
                    for hour, duration in usage_info.items():
                        _update_or_insert_hour(cursor, str(hour), duration)
                
                conn.commit()
                
    except Error as e:
        logging.error(f"Error inserting hourly data for {app_name}: {e}")
        raise

def calculate_hourly_usage(start_time: str, end_time: str) -> Dict[int, int]:
    """Highly optimized hourly usage calculation"""
    start = datetime.datetime.strptime(start_time, "%H:%M:%S")
    end = datetime.datetime.strptime(end_time, "%H:%M:%S")

    if end < start:
        end += datetime.timedelta(days=1)
    
    total_seconds = int((end - start).total_seconds())
    if total_seconds <= 0:
        return {}

    usage_per_hour = {}
    current_hour = start.hour
    
    # Fast path for same hour
    if start.hour == end.hour:
        usage_per_hour[current_hour] = total_seconds
        return usage_per_hour
    
    # Calculate partial hours
    first_hour_seconds = 3600 - (start.minute * 60 + start.second)
    if first_hour_seconds > 0:
        usage_per_hour[current_hour] = first_hour_seconds
    
    current_hour = (current_hour + 1) % 24
    while current_hour != end.hour:
        usage_per_hour[current_hour] = 3600
        current_hour = (current_hour + 1) % 24
    
    last_hour_seconds = end.minute * 60 + end.second
    if last_hour_seconds > 0:
        usage_per_hour[end.hour] = last_hour_seconds

    return usage_per_hour

def insert_Xtra_info(status: bool) -> None:
    """Inserts user's pickup and drop-off details."""
    now = datetime.datetime.now()
    present_date = str(now.today()).split()[0]
    current_time = now.strftime("%I:%M %p")

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                insert_query = "INSERT INTO info (date, status, time) VALUES (%s, %s, %s)"
                values = (present_date, int(status), current_time)
                cursor.execute(insert_query, values)
                conn.commit()
    except Exception as e:
        logging.error(f"Error inserting Xtra info: {e}")

def get_hourly_details(email, serial_id):
    result_dict = {}
    now = datetime.datetime.now()
    present_day = now.strftime("%A")

    query = """
        SELECT app_name, hour, used_time
        FROM app_hour_data
        WHERE email = %s AND used_day = %s AND serial_id = %s
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (email, present_day, serial_id))
                rows = cursor.fetchall()

                if not rows:
                    return None

            for row in rows:
                app_name = row[0]
                hour_used_time = [row[1], row[2]]
                if app_name in result_dict:
                    result_dict[app_name].append(hour_used_time)
                else:
                    result_dict[app_name] = [hour_used_time]

            return result_dict

    except Exception as e:
        logging.error(f"Error getting hourly details: {e}")
        return None

def categorize_batch_apps(app_batch: List[tuple]) -> Dict[str, int]:
    """Categorize apps using Gemini API"""
    app_usage = {app[0]: app[1] for app in app_batch}
    
    logging.info(f"\n=== Starting App Categorization ===")
    logging.info(f"Apps to categorize: {app_usage}")
    
    URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    
    prompt = (
        f"Given these applications and their usage times: {json.dumps(app_usage)}\n"
        f"Categorize them into these exact categories and sum their times:\n"
        f"'Productivity', 'Entertainment', 'Social Networking', 'Other'\n\n"
        f"Detailed Categorization Rules:\n"
        f"1. Productivity Category:\n"
        f"   - Development: VSCode, PyCharm, Eclipse, IntelliJ, Sublime, Atom, Visual Studio\n"
        f"   - Version Control: GitHub, GitLab, Bitbucket\n"
        f"   - Office: Word, Excel, PowerPoint, Google Docs, Sheets, Slides, OneNote\n"
        f"   - Design: Figma, Adobe XD, Photoshop, Illustrator\n"
        f"   - Project Management: Jira, Trello, Asana\n"
        f"   - IDEs and Text Editors: Any coding environment\n"
        f"2. Entertainment Category:\n"
        f"   - Streaming: YouTube, Netflix, Prime Video, Disney+, Twitch\n"
        f"   - Music: Spotify, Apple Music, VLC\n"
        f"   - Games: Steam, Epic Games, Gaming platforms\n"
        f"   - Media: Video players, Music players\n"
        f"3. Social Networking Category:\n"
        f"   - Social Media: Facebook, Instagram, Twitter, LinkedIn, Reddit\n"
        f"   - Messaging: WhatsApp, Telegram, Discord, Slack\n"
        f"   - Video Calls: Zoom, Meet, Teams, Skype\n"
        f"4. Other Category (Only if cannot categorize):\n"
        f"   - System utilities and generic browsers\n"
        f"Important Rules:\n"
        f"- Categorize based on primary purpose\n"
        f"- Browser URLs should be categorized by website purpose\n"
        f"Return ONLY a JSON object with categories and total seconds.\n"
        f"Example: {{'Productivity': 300, 'Entertainment': 150, 'Social Networking': 120, 'Other': 60}}"
    )
    
    payload = {
        "contents": [{
            "role": "user",
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.1,
            "topK": 1,
            "topP": 0.1,
            "maxOutputTokens": 1024
        }
    }
    
    try:
        logging.info("Making Gemini API request...")
        response = requests.post(
            f"{URL}?key={API_KEY}",
            json=payload,
            timeout=10,
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        
        try:
            text = response.json()['candidates'][0]['content']['parts'][0]['text']
            text = text.strip()
            if text.startswith('```'):
                text = text[text.find('{'):text.rfind('}')+1]
            elif not text.startswith('{'):
                text = text[text.find('{'):text.rfind('}')+1]
            
            logging.info(f"Gemini Response: {text}")
            
            categorized_times = json.loads(text)
            validated_times = _validate_times(categorized_times)
            
            logging.info(f"=== Categorization Results ===")
            for category, time in validated_times.items():
                logging.info(f"{category}: {time}s")
            
            return validated_times
            
        except (KeyError, json.JSONDecodeError) as e:
            logging.error(f"Error parsing Gemini response: {e}")
            return {"Other": sum(app_usage.values())}
            
    except Exception as e:
        logging.error(f"Gemini API call failed: {e}")
        return {"Other": sum(app_usage.values())}

def _validate_category(category: str) -> str:
    """Validate and normalize category names"""
    valid_categories = {
        'productivity': 'Productivity',
        'entertainment': 'Entertainment',
        'social networking': 'Social Networking',
        'other': 'Other'
    }
    return valid_categories.get(category.lower(), 'Other')

def _validate_times(times: Dict[str, int]) -> Dict[str, int]:
    """Validate and clean category times"""
    validated = {}
    for category, time in times.items():
        category = _validate_category(category)
        if time > 0:  # Only include positive times
            validated[category] = validated.get(category, 0) + time
    return validated or {'Other': 0}  # Default if empty

