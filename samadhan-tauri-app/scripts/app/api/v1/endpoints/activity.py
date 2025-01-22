from fastapi import APIRouter, HTTPException, Query
from typing import Dict, List
import mysql.connector
from datetime import datetime, timedelta
from app.core.config import settings
from app.db.database import get_db_connection

router = APIRouter()

def get_hourly_details(email: str, serial_id: str) -> Dict[str, Dict[int, float]]:
    categories = {
        "Social Networking": {hour: 0 for hour in range(24)},
        "Entertainment": {hour: 0 for hour in range(24)},
        "Productivity": {hour: 0 for hour in range(24)},
        "Others": {hour: 0 for hour in range(24)},
    }

    query = """
        SELECT app_name, hour, used_time
        FROM app_hour_data
        WHERE email = %s AND used_day = %s AND serial_id = %s
    """
    
    try:
        conn = get_db_connection()
        dbcursor = conn.cursor()
        
        now = datetime.now()
        present_day = now.strftime("%A")
        
        dbcursor.execute(query, (email, present_day, serial_id))
        rows = dbcursor.fetchall()

        if not rows:
            return categories

        for app_name, hour, used_time in rows:
            if app_name in categories:
                # Convert seconds to minutes
                minutes = used_time / 60
                categories[app_name][hour] = minutes

        return categories

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )
    finally:
        if 'dbcursor' in locals():
            dbcursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

@router.get("/daily")
async def get_daily_activity(
    email: str = Query(...),
    serial_id: str = Query(...)
) -> Dict[str, Dict[int, float]]:
    """Get daily activity data directly from categorized data"""
    try:
        return get_hourly_details(email, serial_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get activity data: {str(e)}"
        )

@router.get("/app-usage")
async def get_app_usage(
    email: str = Query(...),
    serial_id: str = Query(...)
) -> Dict:
    """Get top 3 most used apps and their usage info for today"""
    try:
        conn = get_db_connection()
        dbcursor = conn.cursor()

        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        query = """
            SELECT 
                tab_name,
                SUM(used_time) as total_time,
                (SUM(used_time) * 100.0 / (
                    SELECT SUM(used_time)
                    FROM app_usage_info
                    WHERE email = %s 
                    AND serial_id = %s 
                    AND used_date = %s
                )) as percentage
            FROM app_usage_info
            WHERE email = %s 
            AND serial_id = %s 
            AND used_date = %s
            GROUP BY tab_name
            ORDER BY total_time DESC
            LIMIT 3
        """
        
        dbcursor.execute(query, (email, serial_id, today, email, serial_id, today))
        apps = dbcursor.fetchall()

        if not apps:
            return {
                "success": True,
                "data": {
                    "apps": [],
                    "total_time": 0,
                    "comparison": "No data yet"
                }
            }

        total_query = """
            SELECT SUM(used_time)
            FROM app_usage_info
            WHERE email = %s 
            AND serial_id = %s 
            AND used_date = %s
        """
        
        dbcursor.execute(total_query, (email, serial_id, today))
        total_time = dbcursor.fetchone()[0] or 0
        
        dbcursor.execute(total_query, (email, serial_id, yesterday))
        yesterday_total = dbcursor.fetchone()[0] or 0

        diff_minutes = (total_time - yesterday_total) // 60
        if yesterday_total > 0:
            if diff_minutes > 0:
                comparison = f"{diff_minutes // 60}h {diff_minutes % 60}m more than yesterday"
            else:
                abs_diff = abs(diff_minutes)
                comparison = f"{abs_diff // 60}h {abs_diff % 60}m less than yesterday"
        else:
            comparison = "No data from yesterday"

        formatted_apps = [
            {
                "tab_name": name,
                "used_time": time // 60,
                "percentage": round(float(percentage)) if percentage else 0
            }
            for name, time, percentage in apps
        ]

        return {
            "success": True,
            "data": {
                "apps": formatted_apps,
                "total_time": total_time // 60,
                "comparison": comparison
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get app usage data: {str(e)}"
        )
    finally:
        if 'dbcursor' in locals():
            dbcursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def get_date_ranges():
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    # For this week: Get data from Monday to current day
    current_weekday = today.weekday()  # Monday is 0, Sunday is 6
    monday = today - timedelta(days=current_weekday)
    
    return {
        "today": today,
        "yesterday": yesterday,
        "week_start": monday,
        "week_end": today
    }

@router.get("/app-usage-all")
async def get_all_app_usage(email: str, serial_id: str):
    print(f"Received request for email: {email}, serial_id: {serial_id}")
    try:
        # Get today's data
        today_data = get_app_usage_info(email, serial_id, "today")
        print(f"Today's data: {today_data}")

        # Get yesterday's data
        yesterday_data = get_app_usage_info(email, serial_id, "yesterday")
        print(f"Yesterday's data: {yesterday_data}")

        # Get this week's data
        this_week_data = get_app_usage_info(email, serial_id, "this_week")
        print(f"This week's data: {this_week_data}")

        response_data = {
            "success": True,
            "data": {
                "today": today_data,
                "yesterday": yesterday_data,
                "this_week": this_week_data
            }
        }
        print(f"Sending response: {response_data}")
        return response_data
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

def get_app_usage_info(email: str, serial_id: str, period: str) -> Dict:
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        date_ranges = get_date_ranges()
        print(f"Date ranges: {date_ranges}")  # Debug log
        
        # Get the appropriate date based on period
        if period == "today":
            target_date = date_ranges["today"]
            query = """
                SELECT 
                    tab_name as name, 
                    SUM(used_time) as used_time
                FROM app_usage_info
                WHERE email = %s 
                AND serial_id = %s 
                AND (used_date = %s OR used_day = %s)
                GROUP BY tab_name
                ORDER BY used_time DESC
            """
            today_day = target_date.strftime("%A")  # Get day name (Monday, Tuesday, etc.)
            params = (email, serial_id, target_date, today_day)
        elif period == "yesterday":
            target_date = date_ranges["yesterday"]
            query = """
                SELECT 
                    tab_name as name, 
                    SUM(used_time) as used_time
                FROM app_usage_info
                WHERE email = %s 
                AND serial_id = %s 
                AND (used_date = %s OR used_day = %s)
                GROUP BY tab_name
                ORDER BY used_time DESC
            """
            yesterday_day = target_date.strftime("%A")
            params = (email, serial_id, target_date, yesterday_day)
        else:  # this_week
            query = """
                SELECT 
                    tab_name as name, 
                    SUM(used_time) as used_time
                FROM app_usage_info
                WHERE email = %s 
                AND serial_id = %s 
                AND (used_date BETWEEN %s AND %s)
                GROUP BY tab_name
                ORDER BY used_time DESC
            """
            params = (email, serial_id, date_ranges["week_start"], date_ranges["today"])

        print(f"Executing query: {query}")  # Debug log
        print(f"Query params: {params}")    # Debug log
        
        cursor.execute(query, params)
        apps_data = cursor.fetchall()
        print(f"Raw apps data from DB: {apps_data}")  # Debug log

        # Calculate total time
        total_time = sum(app['used_time'] for app in apps_data) if apps_data else 0
        print(f"Total time calculated: {total_time}")  # Debug log

        # If no data found, return empty structure
        if not apps_data:
            print("No data found in database")  # Debug log
            return {
                "apps": [],
                "total_time": 0
            }

        # Process apps data to add logo URLs
        processed_apps = []
        for app in apps_data:
            app_name = app['name']
            # Add default logo URL based on app name
            logo_url = None
            if app_name.lower() in ['chrome', 'google chrome']:
                logo_url = "https://upload.wikimedia.org/wikipedia/commons/e/e1/Google_Chrome_icon_%28February_2022%29.svg"
            elif app_name.lower() in ['firefox', 'mozilla firefox']:
                logo_url = "https://upload.wikimedia.org/wikipedia/commons/a/a0/Firefox_logo%2C_2019.svg"
            elif app_name.lower() in ['spotify']:
                logo_url = "https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg"
            elif app_name.lower() in ['vscode', 'visual studio code']:
                logo_url = "https://upload.wikimedia.org/wikipedia/commons/9/9a/Visual_Studio_Code_1.35_icon.svg"
            elif app_name.lower() in ['cursor']:
                logo_url = "https://cursor.sh/favicon.ico"
            
            processed_apps.append({
                "name": app_name,
                "used_time": int(app['used_time']),  # Convert to int to avoid decimal issues
                "logo_url": logo_url
            })

        result = {
            "apps": processed_apps,
            "total_time": int(total_time)  # Convert to int to avoid decimal issues
        }
        print(f"Final processed result: {result}")  # Debug log
        return result

    except Exception as e:
        print(f"Error in get_app_usage_info: {str(e)}")
        print(f"Error type: {type(e)}")
        print(f"Error args: {e.args}")
        # Return empty structure instead of raising error
        return {
            "apps": [],
            "total_time": 0
        }
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_app_usage_all(
    email: str = Query(..., description="User email"),
    serial_id: str = Query(..., description="Device serial ID")
):
    try:
        if not email or not serial_id:
            raise HTTPException(status_code=400, detail="Email and serial_id are required")
            
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        date_ranges = get_date_ranges()
        
        # Initialize response structure
        response = {
            "success": True,
            "data": {
                "today": {"apps": [], "total_time": 0},
                "yesterday": {"apps": [], "total_time": 0},
                "this_week": {"apps": [], "total_time": 0}
            }
        }
        
        # Function to process apps data with Others category
        def process_apps_data(apps_data):
            if not apps_data:
                return [], 0
                
            # Convert seconds to hours for each app
            processed_apps = [
                {
                    "appName": app["tab_name"],
                    "hours": round(app["total_time"] / 3600, 2),  # Convert seconds to hours
                    "color": ""  # Frontend will handle colors
                }
                for app in apps_data[:5]  # Get top 5 apps
            ]
            
            # Calculate total time in seconds
            total_time = sum(app["total_time"] for app in apps_data)
            
            # Calculate Others if there are more than 5 apps
            if len(apps_data) > 5:
                others_time = sum(app["total_time"] for app in apps_data[5:])
                if others_time > 0:
                    processed_apps.append({
                        "appName": "Others",
                        "hours": round(others_time / 3600, 2),  # Convert seconds to hours
                        "color": ""
                    })
                
            return processed_apps, total_time
        
        # Fetch data for today
        cursor.execute("""
            SELECT tab_name, SUM(used_time) as total_time
            FROM app_usage_info
            WHERE email = %s AND serial_id = %s AND used_date = %s
            GROUP BY tab_name
            ORDER BY total_time DESC
        """, (email, serial_id, date_ranges["today"]))
        
        today_apps = cursor.fetchall()
        processed_today_apps, total_time_today = process_apps_data(today_apps)
        response["data"]["today"]["apps"] = processed_today_apps
        response["data"]["today"]["total_time"] = total_time_today
        
        # Fetch data for yesterday
        cursor.execute("""
            SELECT tab_name, SUM(used_time) as total_time
            FROM app_usage_info
            WHERE email = %s AND serial_id = %s AND used_date = %s
            GROUP BY tab_name
            ORDER BY total_time DESC
        """, (email, serial_id, date_ranges["yesterday"]))
        
        yesterday_apps = cursor.fetchall()
        processed_yesterday_apps, total_time_yesterday = process_apps_data(yesterday_apps)
        response["data"]["yesterday"]["apps"] = processed_yesterday_apps
        response["data"]["yesterday"]["total_time"] = total_time_yesterday
        
        # Fetch data for this week
        cursor.execute("""
            SELECT tab_name, SUM(used_time) as total_time
            FROM app_usage_info
            WHERE email = %s AND serial_id = %s 
            AND used_date BETWEEN %s AND %s
            GROUP BY tab_name
            ORDER BY total_time DESC
        """, (email, serial_id, date_ranges["week_start"], date_ranges["week_end"]))
        
        week_apps = cursor.fetchall()
        processed_week_apps, total_time_week = process_apps_data(week_apps)
        response["data"]["this_week"]["apps"] = processed_week_apps
        response["data"]["this_week"]["total_time"] = total_time_week
        
        cursor.close()
        conn.close()
        
        return response
        
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

@router.get("/weekly-usage")
async def get_weekly_usage(email: str = Query(...), serial_id: str = Query(...)):
    """Get weekly usage data including daily totals and top 3 apps' daily usage"""
    try:
        if not email or not serial_id:
            return {
                "success": False,
                "error": "Email and serial_id are required"
            }

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get current week's date range
        today = datetime.now().date()
        current_weekday = today.weekday()  # Monday is 0, Sunday is 6
        monday = today - timedelta(days=current_weekday)
        
        try:
            # Get daily totals for the week
            daily_totals_query = """
                SELECT 
                    used_date,
                    used_day,
                    SUM(used_time) as total_time
                FROM app_usage_info
                WHERE email = %s 
                AND serial_id = %s 
                AND used_date >= %s
                AND used_date <= %s
                GROUP BY used_date, used_day
                ORDER BY used_date
            """
            cursor.execute(daily_totals_query, (email, serial_id, monday, today))
            daily_totals = cursor.fetchall()
            
            if not daily_totals:
                return {
                    "success": True,
                    "data": {
                        "days": [],
                        "top_apps": []
                    }
                }
            
            # Get top 3 most used apps for the week
            top_apps_query = """
                SELECT 
                    tab_name,
                    SUM(used_time) as total_time
                FROM app_usage_info
                WHERE email = %s 
                AND serial_id = %s 
                AND used_date >= %s
                AND used_date <= %s
                GROUP BY tab_name
                ORDER BY total_time DESC
                LIMIT 3
            """
            cursor.execute(top_apps_query, (email, serial_id, monday, today))
            top_apps = cursor.fetchall()
            
            # Get daily usage for top 3 apps
            app_daily_usage = {}
            for app in top_apps:
                app_name = app['tab_name']
                daily_usage_query = """
                    SELECT 
                        used_date,
                        used_day,
                        SUM(used_time) as used_time
                    FROM app_usage_info
                    WHERE email = %s 
                    AND serial_id = %s 
                    AND tab_name = %s
                    AND used_date >= %s
                    AND used_date <= %s
                    GROUP BY used_date, used_day
                    ORDER BY used_date
                """
                cursor.execute(daily_usage_query, (email, serial_id, app_name, monday, today))
                app_daily_usage[app_name] = cursor.fetchall()
            
            # Format the response
            days = []
            current_date = monday
            while current_date <= today:
                day_data = next(
                    (d for d in daily_totals if d['used_date'].strftime('%Y-%m-%d') == current_date.strftime('%Y-%m-%d')), 
                    None
                )
                days.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'day': current_date.strftime('%A'),
                    'total_time': day_data['total_time'] if day_data else 0
                })
                current_date += timedelta(days=1)
            
            top_apps_data = []
            for app in top_apps:
                app_data = {
                    'name': app['tab_name'],
                    'total_time': app['total_time'],
                    'daily_usage': []
                }
                
                current_date = monday
                while current_date <= today:
                    day_usage = next(
                        (d for d in app_daily_usage[app['tab_name']] 
                         if d['used_date'].strftime('%Y-%m-%d') == current_date.strftime('%Y-%m-%d')), 
                        None
                    )
                    app_data['daily_usage'].append({
                        'date': current_date.strftime('%Y-%m-%d'),
                        'day': current_date.strftime('%A'),
                        'used_time': day_usage['used_time'] if day_usage else 0
                    })
                    current_date += timedelta(days=1)
                
                top_apps_data.append(app_data)
            
            return {
                "success": True,
                "data": {
                    "days": days,
                    "top_apps": top_apps_data
                }
            }

        except mysql.connector.Error as db_error:
            return {
                "success": False,
                "error": f"Database error: {str(db_error)}"
            }

    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get weekly usage data: {str(e)}"
        }
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close() 