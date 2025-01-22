from fastapi import APIRouter, HTTPException, Query
from typing import Dict
import mysql.connector
from datetime import datetime, timedelta
from app.core.config import settings

router = APIRouter()

def get_connection():
    return mysql.connector.connect(
        host=settings.DB_HOST,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME
    )

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
        conn = get_connection()
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
        conn = get_connection()
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