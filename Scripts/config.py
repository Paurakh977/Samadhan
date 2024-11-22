import time
import datetime
from mysql.connector import Error, OperationalError, pooling
from serial_id import get_serial_number

pool = None


def initialize_pool():
    global pool

    try:
        pool = pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=5,
            host="127.0.0.1",
            user="root",
            password="",
            database="samadhandb",
        )
    except OperationalError as e:
        print(f"operational error in inittializing the pool as {e}")
        time.sleep(5)
        initialize_pool()
    except Exception as e:
        print(f"failed to initiaalize pool as {e}")
        time.sleep(5)
        initialize_pool()


def get_connection():
    """Establish and return a new database connection, with infinite retries if needed."""
    attempt = 0
    global pool

    if pool is None:
        initialize_pool()

    while True:
        try:
            connection = pool.get_connection()
            if connection.is_connected():
                print("Connected to MySQL successfully.")
                return connection
        except OperationalError as e:
            attempt += 1
            print(
                f"Attempt {attempt}: Lost connection to MySQL. Retrying... Error: {e}"
            )
            time.sleep(5)
        except Error as e:
            attempt += 1
            print(f"Attempt {attempt}: Database connection failed. Error: {e}")
            time.sleep(5)


def calculate_hourly_usage(start_time: str, end_time: str) -> dict:
    start = datetime.datetime.strptime(start_time, "%H:%M:%S")
    end = datetime.datetime.strptime(end_time, "%H:%M:%S")
    print(start, end)

    if end < start:
        end += datetime.timedelta(days=1)

    usage_per_hour = {}

    current = start
    while current < end:
        next_hour = (current + datetime.timedelta(hours=1)).replace(
            minute=0, second=0, microsecond=0
        )

        if next_hour > end:
            next_hour = end

        seconds_used = int((next_hour - current).total_seconds())
        usage_per_hour[current.hour] = (
            usage_per_hour.get(current.hour, 0) + seconds_used
        )

        current = next_hour

    return usage_per_hour


def insert_Xtra_info(status: bool) -> None:
    """Inserts user's pickup and drop-off details."""
    conn = None
    dbcursor = None

    now = datetime.datetime.now()
    present_date = str(now.today()).split()[0]
    current_time = now.strftime("%I:%M %p")

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
        conn = get_connection()
        dbcursor = conn.cursor()
        dbcursor.execute(query, (email, present_day, serial_id))
        rows = dbcursor.fetchall()

        if rows:
            print(len(rows))
            for row in rows:
                app_name = row[0]
                hour_used_time = [row[1], row[2]]

                if app_name in result_dict:
                    result_dict[app_name].append(hour_used_time)
                else:
                    result_dict[app_name] = [hour_used_time]

            print(len(result_dict))
            return result_dict
        else:
            return None

    except Exception as e:
        print(f"error in getting hourly details as ---> {e}")

    finally:
        if conn.is_connected():
            dbcursor.close()
            conn.close()
            print("MySQL connection is closed")


def insert_app_hourly_info(
    start_time, end_time, used_time, app_name, serial_id, user_email
):
    try:
        conn = get_connection()
        dbcursor = conn.cursor()

        st_hour = start_time.split(":")[0]
        end_hour = end_time.split(":")[0]

        now = datetime.datetime.now()
        present_date = str(now.today()).split()[0]
        present_day = now.strftime("%A")

        def do_if_row_exists(st_hour, used_time=used_time):
            dbcursor.execute(
                "SELECT * FROM app_hour_data WHERE app_name=%s AND used_day=%s AND email=%s AND serial_id = %s AND hour=%s",
                (app_name, present_day, user_email, serial_id, st_hour),
            )

            row = dbcursor.fetchone()

            if row:
                # check that even it is for the same date or not if not delete the previous one
                if (
                    str(row[5]) == str(present_date)
                ):  # This app has already been used for this hour on this day now updated this time
                    new_used_time = int(row[3]) + used_time

                    dbcursor.execute(
                        "UPDATE app_hour_data SET used_time=%s WHERE app_name=%s AND used_day=%s AND email= %s AND serial_id = %s AND hour=%s",
                        (
                            new_used_time,
                            app_name,
                            present_day,
                            user_email,
                            serial_id,
                            st_hour,
                        ),
                    )
                    conn.commit()
                    print(f"data updated for {app_name}")
                    return True

                else:
                    delete_query = (
                        "DELETE FROM app_hour_data WHERE used_day =%s AND email =%s"
                    )
                    dbcursor.execute(delete_query, (present_day, user_email))
                    conn.commit()
                    print("Deleted succesfully")

                    return True

            return False

        def do_if_row_doesnot_exists(st_hour, used_time=used_time):
            try:
                insert_query = "INSERT INTO app_hour_data (app_name, hour, used_time,used_day,used_date,email,serial_id) VALUES (%s, %s, %s,%s,%s,%s,%s)"
                values = (
                    app_name,
                    st_hour,
                    used_time,
                    present_day,
                    present_date,
                    user_email,
                    serial_id,
                )
                dbcursor.execute(insert_query, values)
                print(f"New Data Inserted in the hourly table for {app_name}")
                conn.commit()
                return True
            except Exception as e:
                print(f"error in inserting the hourly data : {e}")
                return False

        if st_hour == end_hour:
            if do_if_row_exists(st_hour):
                print(f"data updated for {app_name} with time : {used_time}")

            else:  # No such row exists from before but start_time_hour== end_time_hour
                print(
                    f"data inserted for {app_name} with time : {used_time}"
                ) if do_if_row_doesnot_exists(st_hour) else None

        else:  # start_time_hour !== end_time_hour
            usage_info_dict = calculate_hourly_usage(start_time, end_time)
            print(f"MY DICITONARY: ---> {usage_info_dict}")
            for keys, values in usage_info_dict.items():
                if do_if_row_exists(st_hour=keys, used_time=values):
                    print(f"----data updated for {app_name} with time : {values}----")
                else:
                    do_if_row_doesnot_exists(st_hour=keys, used_time=values)
                    print(f"-----data inserted for {app_name} with time : {values}----")

    except Exception as e:
        print(f"problem in insert_app_hourly_info function :{e}")
    finally:
        if conn.is_connected():
            dbcursor.close()
            conn.close()
            print("MySQL connection is closed")


def insert_app_info(tab_name, used_time, user_email, serial_id):
    try:
        conn = get_connection()
        dbcursor = conn.cursor()

        now = datetime.datetime.now()
        present_date = str(now.today()).split()[0]
        present_day = now.strftime("%A")

        dbcursor.execute(
            "SELECT * FROM app_usage_info WHERE tab_name=%s AND used_day=%s AND email=%s AND serial_id = %s",
            (tab_name, present_day, user_email, serial_id),
        )
        row = dbcursor.fetchone()

        if row:
            if str(row[5]) == str(present_date):
                new_used_time = int(row[1]) + used_time
                dbcursor.execute(
                    "UPDATE app_usage_info SET used_time=%s WHERE tab_name=%s AND used_day=%s AND email= %s AND serial_id = %s",
                    (new_used_time, tab_name, present_day, user_email, serial_id),
                )
                conn.commit()
                print("data updated")
            else:
                delete_query = (
                    "DELETE FROM app_usage_info WHERE used_day =%s AND email =%s"
                )
                dbcursor.execute(delete_query, (present_day, user_email))
                conn.commit()
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
            conn.commit()
            print("New Data Inserted")

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
