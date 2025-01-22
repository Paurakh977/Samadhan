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
        
        # Get the appropriate date based on period
        if period == "today":
            target_date = date_ranges["today"]
            query = """
                SELECT tab_name, SUM(used_time) as total_time
                FROM app_usage_info
                WHERE email = %s AND serial_id = %s AND used_date = %s
                GROUP BY tab_name
                ORDER BY total_time DESC
            """
            params = (email, serial_id, target_date)
        elif period == "yesterday":
            target_date = date_ranges["yesterday"]
            query = """
                SELECT tab_name, SUM(used_time) as total_time
                FROM app_usage_info
                WHERE email = %s AND serial_id = %s AND used_date = %s
                GROUP BY tab_name
                ORDER BY total_time DESC
            """
            params = (email, serial_id, target_date)
        else:  # this_week
            query = """
                SELECT tab_name, SUM(used_time) as total_time
                FROM app_usage_info
                WHERE email = %s AND serial_id = %s 
                AND used_date BETWEEN %s AND %s
                GROUP BY tab_name
                ORDER BY total_time DESC
            """
            params = (email, serial_id, date_ranges["week_start"], date_ranges["week_end"])
        
        cursor.execute(query, params)
        apps = cursor.fetchall()
        
        # Process the apps data
        processed_apps = []
        total_time = 0
        
        for app in apps:
            total_time += app['total_time']
            processed_apps.append({
                "name": app['tab_name'],
                "used_time": app['total_time']
            })
        
        return {
            "apps": processed_apps,
            "total_time": total_time
        }
        
    except Exception as e:
        print(f"Error in get_app_usage_info: {str(e)}")
        return {
            "apps": [],
            "total_time": 0
        }
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
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