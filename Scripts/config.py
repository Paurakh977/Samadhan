import mysql.connector
import datetime
from mysql.connector import Error
from serial_id import get_serial_number


# global variables

now = datetime.datetime.now()
present_date = str(now.today()).split()[0]
present_day = now.strftime("%A")
current_time = now.strftime("%I:%M %p")


def get_connection():
    """Establish and return a new database connection."""
    return mysql.connector.connect(
        host="localhost", user="root", password="", database="samadhandb"
    )


def insert_Xtra_info(status: bool) -> None:
    """Inserts user's pickup and drop-off details."""
    conn = None
    dbcursor = None

    try:
        conn = get_connection()
        dbcursor = conn.cursor()

        insert_query = "INSERT INTO info (date, status, time) VALUES (%s, %s, %s)"
        values = (present_date, int(status), current_time)

        dbcursor.execute(insert_query, values)
        conn.commit()

    except Exception as e:
        print(f"Error: {e}\nCould not insert pickup and drop-off details")

    finally:
        if dbcursor is not None:
            dbcursor.close()
        if conn is not None:
            conn.close()


def insert_app_info(tab_name, used_time, user_email, serial_id):
    try:
        conn = get_connection()
        dbcursor = conn.cursor()

        dbcursor.execute(
            "SELECT * FROM app_usage_info WHERE tab_name=%s AND used_day=%s AND email=%s AND serial_id = %s",
            (tab_name, present_day, user_email, serial_id),
        )
        row = dbcursor.fetchone()

        if row:
            if str(row[5]) == str(present_date):
                used_time = row[1] + 3
                dbcursor.execute(
                    "UPDATE app_usage_info SET used_time=%s WHERE tab_name=%s AND used_day=%s AND email= %s AND serial_id = %s",
                    (used_time, tab_name, present_day, user_email, serial_id),
                )
                print("data updated")
            else:
                delete_query = (
                    "DELETE FROM app_usage_info WHERE used_day =%s AND email =%s"
                )
                dbcursor.execute(delete_query, (present_day, user_email))
                print("Deleted succesfully")
        else:
            insert_query = "INSERT INTO app_usage_info (tab_name, used_time, email,used_day,used_date,serial_id) VALUES (%s, %s, %s,%s,%s,%s)"
            values = (
                tab_name,
                used_time,
                user_email,
                present_day,
                present_date,
                serial_id,
            )
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


def insert_manual_users(name, email, phone, password, serail_id, radio):
    conn = get_connection()
    dbcursor = conn.cursor()
    records_query = records_query = (
        "(SELECT email FROM user_info_manual WHERE email=%s) UNION (SELECT email FROM user_info_google WHERE email=%s);"
    )
    dbcursor.execute(records_query, (email, email))
    records = dbcursor.fetchone()

    if not records:
        query = "INSERT INTO user_info_manual (username, phnumber, email, password, radio_button, serial_id) values (%s, %s,%s, %s,%s, %s)"
        dbcursor.execute(query, (name, phone, email, password, radio, serail_id))
        conn.commit()
        conn.close()
        return True
    else:
        conn.commit()
        conn.close()
        return False


def insert_user(name, email, serial_id):
    conn = get_connection()
    dbcursor = conn.cursor()
    records_query = "SELECT * FROM user_info_google  WHERE email=%s"
    dbcursor.execute(records_query, (email,))

    records = dbcursor.fetchone()

    if not records:
        query = "INSERT INTO user_info_google(username, email, serial_id) values (%s, %s, %s)"
        dbcursor.execute(query, (name, email, serial_id))
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
    records_query = "SELECT * FROM user_info_google  WHERE email= %s "
    dbcursor.execute(records_query, (email,))
    records = dbcursor.fetchone()

    if records:
        records_query = (
            "SELECT * FROM user_info_google WHERE email = %s AND serial_id = %s"
        )
        dbcursor.execute(records_query, (email, serial_id))
        results = dbcursor.fetchall()
        if results:
            update_query = "UPDATE user_info_google SET logged_in_status = 1 WHERE email= %s AND serial_id = %s"
            dbcursor.execute(update_query, (email, serial_id))

            update_query = "UPDATE user_info_google SET logged_in_status = 0 WHERE email = %s AND serial_id != %s"
            dbcursor.execute(update_query, (email, serial_id))

            query = "SELECT username FROM user_info_google WHERE email = %s"
            dbcursor.execute(query, (email,))
            record = dbcursor.fetchone()
            conn.commit()
            conn.close()
            if record:
                name = record[0]
                print(name)
                return True, name
        else:
            print("block 2")
            query = "SELECT username FROM user_info_google WHERE email = %s "
            dbcursor.execute(query, (email,))
            record = dbcursor.fetchone()

            if record:
                print("about 2 insert")
                name = record[0]
                insert_query = """INSERT INTO user_info_google(username, email, serial_id)  VALUES (%s, %s, %s)"""
                dbcursor.execute(insert_query, (name, email, serial_id))
                update_query = "UPDATE user_info_google SET logged_in_status = 1 WHERE email= %s AND serial_id = %s"
                dbcursor.execute(update_query, (email, serial_id))
                update_query = "UPDATE user_info_google SET logged_in_status = 0 WHERE email = %s AND serial_id != %s"
                dbcursor.execute(update_query, (email, serial_id))
                conn.commit()
                conn.close()
                return True, name
    else:
        print("We didn't find any account matching with the entered credentials.")
        conn.close()
        return False, None

    conn.commit()
    conn.close()


def handel_manual_login(email, password, serail_id):
    conn = get_connection()
    dbcursor = conn.cursor(buffered=True)
    records_query = "SELECT * FROM user_info_manual WHERE email = %s AND password = %s"
    dbcursor.execute(records_query, (email, password))
    records = dbcursor.fetchone()

    if records:
        print(serail_id)
        records_query = (
            "SELECT * FROM user_info_manual WHERE email = %s AND serial_id = %s"
        )
        dbcursor.execute(records_query, (email, serail_id))
        results = dbcursor.fetchall()

        if results:
            print("block 1")
            update_query = "UPDATE user_info_manual SET logged_in_status = 1 WHERE email= %s AND serial_id = %s"
            dbcursor.execute(update_query, (email, serail_id))

            update_query = "UPDATE user_info_manual SET logged_in_status = 0 WHERE email = %s AND serial_id != %s"
            dbcursor.execute(update_query, (email, serail_id))

            query = "SELECT username FROM user_info_manual WHERE email = %s AND password = %s"
            dbcursor.execute(query, (email, password))
            record = dbcursor.fetchone()
            conn.commit()
            conn.close()
            if record:
                name = record[0]
                print(name)
                return True, name
        else:
            print("block 2")
            query = "SELECT username, phnumber, radio_button FROM user_info_manual WHERE email = %s AND password = %s"
            dbcursor.execute(query, (email, password))
            record = dbcursor.fetchone()

            if record:
                print("about 2 insert")
                name, phone, radio = record
                insert_query = """INSERT INTO user_info_manual (username, phnumber, email, password, radio_button, serial_id)  VALUES (%s, %s, %s, %s, %s, %s)"""
                dbcursor.execute(
                    insert_query, (name, phone, email, password, radio, serail_id)
                )
                update_query = "UPDATE user_info_manual SET logged_in_status = 1 WHERE email= %s AND serial_id = %s"
                dbcursor.execute(update_query, (email, serail_id))
                update_query = "UPDATE user_info_manual SET logged_in_status = 0 WHERE email = %s AND serial_id != %s"
                dbcursor.execute(update_query, (email, serail_id))
                conn.commit()
                conn.close()
                return True, name

    else:
        print("We didn't find any account matching with the entered credentials.")
        conn.close()
        return False, None


def get_login_status():
    conn = get_connection()
    dbcursor = conn.cursor()
    records_query = (
        "SELECT * FROM user_info_google WHERE serial_id = %s AND logged_in_status = 1"
    )
    serial_id = get_serial_number()
    dbcursor.execute(records_query, (serial_id,))
    records = dbcursor.fetchone()
    if records:
        conn.close()
        return True, records[2], records[1]
    else:
        records_query = "SELECT * FROM user_info_manual WHERE serial_id = %s AND logged_in_status = 1"
        serial_id = get_serial_number()
        dbcursor.execute(records_query, (serial_id,))
        records = dbcursor.fetchone()
        if records:
            conn.close()

            return True, records[1], records[3]
        else:
            conn.close()
            return False, None, None


def logout_user(email):
    conn = get_connection()
    dbcursor = conn.cursor()

    update_query = "UPDATE user_info_google SET logged_in_status = 0 WHERE email= %s"
    dbcursor.execute(update_query, (email,))
    conn.commit()

    update_query = "UPDATE user_info_manual SET logged_in_status = 0 WHERE email= %s"
    dbcursor.execute(update_query, (email,))
    conn.commit()

    conn.close()
    print(f"{email} logged out")
