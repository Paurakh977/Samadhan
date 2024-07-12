import mysql.connector
import datetime
from mysql.connector import Error
from serial_id import get_serial_number
def get_connection():
    """Establish and return a new database connection."""
    return mysql.connector.connect(
        host="sql12.freesqldatabase.com",
        user="sql12719283",
        password="DZ7mIqLCi7",
        database="sql12719283"
    )
    


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

def insert_manual_users(name,email,phone,password,serail_id,radio):
    conn = get_connection()
    dbcursor = conn.cursor()
    records_query = records_query = "(SELECT email FROM user_info_manual WHERE email=%s) UNION (SELECT email FROM user_info_google WHERE email=%s);"
    dbcursor.execute(records_query, (email,email))
    records = dbcursor.fetchone()    
    
    if not records:
        query= "INSERT INTO user_info_manual (username, phnumber, email, password, radio_button, serial_id) values (%s, %s,%s, %s,%s, %s)"
        dbcursor.execute(query,(name,phone,email,password,radio,serail_id))
        conn.commit()
        conn.close()
        return True
    else:
        conn.commit()
        conn.close()
        return False

    

def insert_user(name,email,serial_id):
    conn = get_connection()
    dbcursor = conn.cursor()
    records_query = "SELECT * FROM user_info_google  WHERE email=%s"
    dbcursor.execute(records_query, (email,))

    records = dbcursor.fetchone()    
    
    if not records:
        query = "INSERT INTO user_info_google(username, email, serial_id) values (%s, %s, %s)"        
        dbcursor.execute(query,(name,email,serial_id))
        conn.commit()
        conn.close()
        return True
    else:
        conn.commit()
        conn.close()
        return False
    

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


def handel_manual_login(email,password,serail_id):
    conn = get_connection()
    dbcursor = conn.cursor()
    records_query = "SELECT * FROM user_info_manual WHERE email = %s AND password = %s"
    dbcursor.execute(records_query, (email,password))
    records = dbcursor.fetchone() 
    
    if records:
        update_query = "UPDATE user_info_manual SET logged_in_status = 1 WHERE email= %s AND serial_id = %s"
        dbcursor.execute(update_query,(email,serail_id))
        conn.commit()
        
        update_query="UPDATE user_info_manual SET logged_in_status = 0 WHERE email = %s AND serial_id != %s"
        dbcursor.execute(update_query,(email,serail_id))
        conn.commit()
        
        query="SELECT username FROM user_info_manual WHERE email = %s AND password = %s"
        dbcursor.execute(query,(email,password))
        record = dbcursor.fetchone()
        if record:
            name= record[0] 
            print(name)
        return True,name
    conn.close()
    return False,None
    
    
def get_login_status():
    conn=get_connection()
    dbcursor = conn.cursor()
    records_query = "SELECT * FROM user_info_google WHERE serial_id = %s AND logged_in_status = 1"
    serial_id=get_serial_number()
    dbcursor.execute(records_query,(serial_id,))
    records = dbcursor.fetchone() 
    if records:
        conn.close()
        return True,records[2],records[1]
    else:
        records_query = "SELECT * FROM user_info_manual WHERE serial_id = %s AND logged_in_status = 1"
        serial_id=get_serial_number()
        dbcursor.execute(records_query,(serial_id,))
        records = dbcursor.fetchone() 
        if records:
            conn.close()
            
            return True,records[1],records[3]
        else:
            conn.close()
            return False,None,None
    
    
def logout_user(email):
    conn=get_connection()
    dbcursor = conn.cursor()
  
    update_query = "UPDATE user_info_google SET logged_in_status = 0 WHERE email= %s"
    dbcursor.execute(update_query,(email,))
    conn.commit()

    update_query = "UPDATE user_info_manual SET logged_in_status = 0 WHERE email= %s"
    dbcursor.execute(update_query,(email,))
    conn.commit()
       
    conn.close()
    print(f"{email} logged out")
    
    




