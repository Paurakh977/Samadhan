import mysql.connector
import datetime
from mysql.connector import Error

def get_connection():
    """Establish and return a new database connection."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="samadhandb"
    )
    
conn = get_connection()
dbcursor = conn.cursor()

def insert(tab_name, used_time, browser):
    try:
        conn = get_connection()
        dbcursor = conn.cursor()
        now = datetime.datetime.now()
        present_date = datetime.date.today()
        present_day = now.strftime("%A")        
        dbcursor.execute("SELECT * FROM app_usage_info WHERE tab_name=%s AND used_day=%s", (tab_name,present_day))
        row = dbcursor.fetchone()
        
        if row : 
            if row[5] == present_date:
                used_time = row[1] + 1  
                dbcursor.execute("UPDATE app_usage_info SET used_time=%s WHERE tab_name=%s AND used_day=%s", (used_time, tab_name, present_day))
                print("data updated")
            else: 
                delete_query = "DELETE FROM app_usage_info WHERE used_day =%s"
                dbcursor.execute(delete_query,(present_day,))
                print("Deleted succesfully")
        else:
            insert_query = "INSERT INTO app_usage_info (tab_name, used_time, browser,used_day,used_date) VALUES (%s, %s, %s,%s,%s)"
            values = (tab_name, used_time, browser,present_day,present_date)
            dbcursor.execute(insert_query, values)
            print("New Data Inserted")

        conn.commit()
    
    except Error as e:
        print(f"Error: {e}")
    
    finally:
        if conn.is_connected():
            dbcursor.close()
            conn.close()
            print("MySQL connection is closed")

def insert_user(name,email,account_type):
    conn = get_connection()
    dbcursor = conn.cursor()
    records_query = "SELECT * FROM user_info  WHERE email=%s"
    dbcursor.execute(records_query, (email,))

    records = dbcursor.fetchone()    
    
    if not records:
        if account_type == "Google":
            query = "INSERT INTO user_info(username, email, account_type) values (%s, %s, %s)"        
            dbcursor.execute(query,(name,email,account_type))
            print("Signed up successfully.")
    else:
        print("There is already an account associated with the chosen google account.")
    conn.commit()
    conn.close()

def handle_google_login(email):  
    conn = get_connection()
    dbcursor = conn.cursor()
    records_query = "SELECT * FROM user_info  WHERE email= %s "
    dbcursor.execute(records_query, (email,))
    records = dbcursor.fetchone()    
    
    if records:
        print("Logged in succesfully.")
        
    else:
        print("We couldn't find any account associated with the google account.")
    
    conn.close()

    




