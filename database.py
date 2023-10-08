import mysql.connector


def connect_to_mysql(host, user, password):
    conn = None
    try:
        conn = mysql.connector.connect(host=host, user=user, password=password)
    except mysql.connector.Error as err:
        print("Error while trying to connect to the database..", err)
    cursor = conn.cursor(dictionary=True)
    print("Success in connecting to MySQL")
    return cursor


def execute_sql_file(cursor):
    try:
        with open("sql/create_db.sql", "r") as sql_file:
            res_iterator = cursor.execute(sql_file.read(), multi=True)
            for res in res_iterator:
                print("Running query... ", res)
                print(f"Rows affected - {res.rowcount}")
    except IOError as err:
        print("Issues with getting sql file")


# TODO function that checks if the DB already exists
# TODO function that checks if the table/s already exists, to allow sql execution
