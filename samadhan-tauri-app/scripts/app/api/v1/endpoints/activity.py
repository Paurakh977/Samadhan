from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Dict, List, Optional
import mysql.connector
from datetime import datetime
import subprocess
import json
import os
from app.core.config import settings
from app.core.deps import get_current_user

router = APIRouter()

def get_connection():
    return mysql.connector.connect(
        host=settings.DB_HOST,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME
    )

def get_hourly_details(email: str, serial_id: str) -> Optional[Dict[str, List]]:
    result_dict = {}
    now = datetime.now()
    present_day = now.strftime("%A")

    query = """
        SELECT app_name, hour, used_time
        FROM app_hour_data
        WHERE email = %s AND used_day = %s AND serial_id = %s
    """
    
    try:
        conn = get_connection()
        dbcursor = conn.cursor()
        dbcursor.execute(query, (email, present_day, serial_id))
        rows = dbcursor.fetchall()

        if rows:
            for row in rows:
                app_name = row[0]
                hour_used_time = [row[1], row[2]]

                if app_name in result_dict:
                    result_dict[app_name].append(hour_used_time)
                else:
                    result_dict[app_name] = [hour_used_time]

            return result_dict
        return None

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

def filtering_data(
    raw_prompt_dict: Dict[str, List[int]],
    categorized_prompt_dict: Dict[str, List[str]],
) -> Dict[str, Dict[int, float]]:
    data = {
        "Social Networking": {hour: 0 for hour in range(24)},
        "Entertainment": {hour: 0 for hour in range(24)},
        "Productivity": {hour: 0 for hour in range(24)},
        "Others": {hour: 0 for hour in range(24)},
    }

    seconds_to_minutes = lambda seconds: round(seconds / 60, 2)

    for app, usage in raw_prompt_dict.items():
        for hour, seconds in usage:
            minutes = seconds_to_minutes(seconds)

            categorized = False
            for category, app_list in categorized_prompt_dict.items():
                if app in app_list:
                    data[category][hour] += minutes
                    categorized = True
                    break

            if not categorized:
                data["Others"][hour] += minutes

    return data

def categorize_app(input_prompt_dict: Dict[str, List]) -> Optional[Dict[str, Dict[int, float]]]:
    categories = ["Social Networking", "Entertainment", "Productivity", "Others"]
    current_directory = os.path.dirname(os.path.abspath(__file__))
    sh_script = os.path.join(current_directory, "parsher.sh")

    formatted_input = f"Hey gemini, here are the categories {categories} and these are some of the names of the applications {list(input_prompt_dict.keys())}. Categorize which application falls under which category yourself. Please do not put any apps in 'Others' if they can be categorized elsewhere. I want you to return a dictionary where keys are the categories and the values are the list of the apps for each category. JUST GIVE ME THE DICT IN RESPONSE NO OTHER INFORMATION OR TEXT"

    try:
        result = subprocess.run(
            ["bash", sh_script, formatted_input], 
            stdout=subprocess.PIPE, 
            text=True,
            check=True
        )

        data = result.stdout.strip()
        parsed_data = json.loads(data)
        text_value = parsed_data["candidates"][0]["content"]["parts"][0]["text"]
        
        cleaned_text = (
            text_value.replace("app_categories =", "")
            .replace("json", "")
            .replace("```python", "")
            .replace("```", "")
            .replace("print(app_categories)", "")
            .strip()
        )

        cleaned_text = cleaned_text.replace("'", '"')
        my_dict = json.loads(cleaned_text)
        return filtering_data(input_prompt_dict, my_dict)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in categorization: {str(e)}"
        )

@router.get("/daily")
async def get_daily_activity(
    email: str = Query(...),
    serial_id: str = Query(...)
) -> Dict[str, Dict[int, float]]:
    """Get daily activity data categorized by app type"""
    try:
        raw_data = get_hourly_details(email, serial_id)
        if not raw_data:
            return {
                "Social Networking": {hour: 0 for hour in range(24)},
                "Entertainment": {hour: 0 for hour in range(24)},
                "Productivity": {hour: 0 for hour in range(24)},
                "Others": {hour: 0 for hour in range(24)},
            }
        
        categorized_data = categorize_app(raw_data)
        if not categorized_data:
            raise HTTPException(
                status_code=500,
                detail="Failed to categorize app data"
            )
            
        return categorized_data
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get activity data: {str(e)}"
        ) 