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
    

def handle_google_login(email, serial_id):
    conn = get_connection()
    dbcursor = conn.cursor()

    try:
        # Check if the user exists
        records_query = "SELECT * FROM user_info_google WHERE email = %s"
        dbcursor.execute(records_query, (email,))
        records = dbcursor.fetchall()

        if records:
            # Check if the user has logged in with this serial ID before
            records_query = "SELECT * FROM user_info_google WHERE email = %s AND serial_id = %s"
            dbcursor.execute(records_query, (email, serial_id))
            results = dbcursor.fetchall()

            if results:
                # This ID has already been registered through this device
               
                while dbcursor.nextset():
                    pass

                update_query_1 = "UPDATE user_info_google SET logged_in_status = 1 WHERE email = %s AND serial_id = %s"
                dbcursor.execute(update_query_1, (email, serial_id))
                conn.commit()

                update_query_2 = "UPDATE user_info_google SET logged_in_status = 0 WHERE email = %s AND serial_id != %s"
                dbcursor.execute(update_query_2, (email, serial_id))
                conn.commit()

                query = "SELECT username FROM user_info_google WHERE email = %s"
                dbcursor.execute(query, (email,))
                record = dbcursor.fetchone()

                # Ensure all results are fetched before returning
                while dbcursor.nextset():
                    pass

                if record:
                    name = record[0]
                    return True, name

            else:
                # Block 2 is assumed to be working correctly
                query = "SELECT username FROM user_info_google WHERE email = %s"
                dbcursor.execute(query, (email,))
                record = dbcursor.fetchone()

                if record:
                    name = record[0]
                    # Ensure all results are fetched before continuing
                    while dbcursor.nextset():
                        pass

                    insert_query = "INSERT INTO user_info_google(username, email, serial_id) values (%s, %s, %s)"
                    dbcursor.execute(insert_query, (name, email, serial_id))
                    conn.commit()

                    update_query = "UPDATE user_info_google SET logged_in_status = 1 WHERE email = %s AND serial_id = %s"
                    dbcursor.execute(update_query, (email, serial_id))
                    conn.commit()
                    
                    update_query = "UPDATE user_info_google SET logged_in_status = 0 WHERE email = %s AND serial_id != %s"
                    dbcursor.execute(update_query, (email, serial_id))
                    conn.commit()

                    return True, name
        else:
            print("User does not exist")
            return False, None

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        conn.rollback()  # Rollback changes if any error occurs
        return False, None

    finally:
        dbcursor.close()
        conn.close()

    return False, None








def handel_manual_login(email,password,serail_id):
    conn = get_connection()
    dbcursor = conn.cursor(buffered=True)
    records_query = "SELECT * FROM user_info_manual WHERE email = %s AND password = %s"
    dbcursor.execute(records_query, (email,password))
    records = dbcursor.fetchone() 
    
    if records:
        records_query = "SELECT * FROM user_info_manual WHERE email = %s AND serial_id = %s"
        dbcursor.execute(records_query, (email,serail_id))
        results = dbcursor.fetchall() 
        
        if results:
            update_query = "UPDATE user_info_manual SET logged_in_status = 1 WHERE email= %s AND serial_id = %s"
            dbcursor.execute(update_query,(email,serail_id))
            
            update_query="UPDATE user_info_manual SET logged_in_status = 0 WHERE email = %s AND serial_id != %s"
            dbcursor.execute(update_query,(email,serail_id))
            
            query="SELECT username FROM user_info_manual WHERE email = %s AND password = %s"
            dbcursor.execute(query,(email,password))
            record = dbcursor.fetchone()
            conn.commit()
            conn.close()
            if record:
                name= record[0] 
                return True,name
        else:
            query = "SELECT username, phnumber, radio_button FROM user_info_manual WHERE email = %s AND password = %s"
            dbcursor.execute(query, (email, password))
            record = dbcursor.fetchone()
            
            if record:
                name,phone,radio=record
                insert_query = """INSERT INTO user_info_manual (username, phnumber, email, password, radio_button, serial_id)  VALUES (%s, %s, %s, %s, %s, %s)"""
                dbcursor.execute(insert_query, (name, phone, email, password, radio, serail_id))
                update_query = "UPDATE user_info_manual SET logged_in_status = 1 WHERE email= %s AND serial_id = %s"
                dbcursor.execute(update_query,(email,serail_id))
                update_query="UPDATE user_info_manual SET logged_in_status = 0 WHERE email = %s AND serial_id != %s"
                dbcursor.execute(update_query,(email,serail_id))
                conn.commit()
                conn.close()
                return True,name

    else:
        print("We didn't find any account matching with the entered credentials.")
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
    
    




