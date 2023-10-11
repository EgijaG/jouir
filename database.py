import mysql.connector

db_creds = {"host": "", "user": "", "password": "", "db": ""}


def set_credentials(host, user, password, db):
    db_creds["host"] = host
    db_creds["user"] = user
    db_creds["password"] = password
    db_creds["db"] = db


def connect_to_mysql():
    try:
        conn = mysql.connector.connect(
            host=db_creds["host"], user=db_creds["user"], password=db_creds["password"]
        )
        if conn.is_connected():
            print("Connected to MySQL Server")
            cursor = conn.cursor(dictionary=True)
            if not database_exists(cursor, db_creds["db"]):
                print("No database <posts> found...")
                execute_sql_file(cursor, "sql/create_db.sql")
            else:
                print("Creating tables...")
                conn.connect(database=db_creds["db"])
                if table_exists(cursor, db_creds["db"], "posts_with_votes"):
                    execute_sql_file(cursor, "sql/create_tables.sql")
                    print("Success in creating tables")

    except mysql.connector.Error as err:
        print("Error while trying to connect to the database..", err)


def execute_sql_file(cursor, file):
    try:
        with open(file, "r") as sql_file:
            res_iterator = cursor.execute(sql_file.read(), multi=True)
            for res in res_iterator:
                print("Running query... ", res)
                print(f"Rows affected - {res.rowcount}")
    except IOError as err:
        print("Issues with getting sql file", err)


# function that checks if the DB already exists
def database_exists(cursor, db_name):
    try:
        cursor.execute(
            "SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = %s",
            (db_name,),
        )
        result = cursor.fetchone()
        if result:
            print("Found database ", db_name)
            return True
    except mysql.connector.Error as err:
        print("Error checking if DB exists. ", err)
    return False


# function that checks if the table/s already exists, to allow sql execution
def table_exists(cursor, db_name, table_name):
    try:
        cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = %s AND table_name = %s",
            (db_name, table_name),
        )
        result = cursor.fetchone()
        if result:
            print("Found table ", table_name)
            return True
    except mysql.connector.Error as err:
        print("Error checking if table exists. ", err)
    return False


# TODO create a function that inserts data into table, that has been received from StackOverFlow
def insert_data(cursor, post):
    try:
        print("Attempting to insert data ...")
        insert_query = (
            "INSERT INTO posts_with_votes (title, url, excerpt_text) VALUES (%(title)s, %(url)s, "
            "%(excerpt)s)"
        )
        cursor.execute(
            insert_query,
            {"title": post.title, "url": post.url, "excerpt_text": post.excerpt},
        )
    except mysql.connector.Error as err:
        print("Error inserting data ", err)
