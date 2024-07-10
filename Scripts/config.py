import mysql.connector
import datetime
from mysql.connector import Error
from serial_id import get_serial_number
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

def insert_user(name,email,serial_id):
    conn = get_connection()
    dbcursor = conn.cursor()
    records_query = "SELECT * FROM user_info_google  WHERE email=%s"
    dbcursor.execute(records_query, (email,))

    records = dbcursor.fetchone()    
    
    if not records:
        query = "INSERT INTO user_info_google(username, email, serial_id) values (%s, %s, %s)"        
        dbcursor.execute(query,(name,email,serial_id))
        print("Signed up successfully.")
    else:
        print("There is already an account associated with the chosen google account.")
    conn.commit()
    conn.close()

def handle_google_login(email):  
    conn = get_connection()
    dbcursor = conn.cursor()
    records_query = "SELECT * FROM user_info_google  WHERE email= %s "
    dbcursor.execute(records_query, (email,))
    records = dbcursor.fetchone() 
       
    if records:
        serial_id=get_serial_number()
        
        update_query = "UPDATE user_info_google SET logged_in_status = 1 WHERE email= %s AND serial_id = %s"
        dbcursor.execute(update_query,(email,serial_id))
        conn.commit()
        
        update_query="UPDATE user_info_google SET logged_in_status = 0 WHERE email = %s AND serial_id != %s"
        dbcursor.execute(update_query,(email,serial_id))
        conn.commit()
        return True
    conn.close()
    return False

def get_login_status():
    conn=get_connection()
    dbcursor = conn.cursor()
    records_query = "SELECT * FROM user_info_google WHERE serial_id = %s AND logged_in_status = 1"
    serial_id=get_serial_number()
    dbcursor.execute(records_query,(serial_id,))
    records = dbcursor.fetchone() 
    conn.close()  
    if records:
        return True,records[2],records[1]
    else:
        return False,None,None
    
def logout_user(email):
    conn=get_connection()
    dbcursor = conn.cursor()
    update_query = "UPDATE user_info_google SET logged_in_status = 0 WHERE email= %s"
    dbcursor.execute(update_query,(email,))
    conn.commit()
    conn.close()
    print(f"{email} logged out")
    
    




