import mysql.connector

db_creds = {"host": "", "user": "", "password": "", "db": ""}
posts = []
connection = None


def set_credentials(db_config):
    db_creds["host"] = db_config["host"]
    db_creds["user"] = db_config["user"]
    db_creds["password"] = db_config["pass"]
    db_creds["db"] = db_config["database"]


def connect_to_mysql():
    global connection
    try:
        connection = mysql.connector.connect(
            host=db_creds["host"], user=db_creds["user"], password=db_creds["password"]
        )
        if connection.is_connected():
            print("Connected to MySQL Server")
            cursor = connection.cursor(dictionary=True)
            if not database_exists(cursor, db_creds["db"]):
                print("No database <posts> found...")
                execute_sql_file(cursor, "sql/create_db.sql")
            else:
                print("Creating tables...")
                connection.connect(database=db_creds["db"])
                if not table_exists(cursor, db_creds["db"], "posts_with_votes"):
                    execute_sql_file(cursor, "sql/create_tables.sql")
                    print("Success in creating tables...")
    except mysql.connector.Error as err:
        print("Error while trying to connect to the database..", err)
    else:
        return connection.cursor(dictionary=True)


def execute_sql_file(cursor, file):
    try:
        with open(file, "r") as sql_file:
            res_iterator = cursor.execute(sql_file.read(), multi=True)
            for res in res_iterator:
                print("Running query... ", res)
                print(f"Rows affected - {res.rowcount}")
    except IOError as err:
        print(f"Issues with getting sql file", err)


# function that checks if the DB already exists
def database_exists(cursor, db_name):
    try:
        cursor.execute(
            "SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = %s",
            (db_name,),
        )
        result = cursor.fetchone()
        if result:
            print(f"Found database ", db_name)
            return True
    except mysql.connector.Error as err:
        print(f"Error checking if DB exists. ", err)
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
            print(f"Found table ", table_name)
            return True
    except mysql.connector.Error as err:
        print(f"Error checking if table exists. ", err)
    return False


def insert_data(cursor, post):
    try:
        print("Attempting to insert data ...")
        insert_query = (
            "INSERT INTO posts_with_votes (title, url, excerpt_text) VALUES (%(title)s, %(url)s, "
            "%(excerpt_text)s)"
        )
        cursor.execute(
            insert_query,
            {"title": post.title, "url": post.url, "excerpt_text": post.excerpt},
        )
        cursor.execute("COMMIT")
    except mysql.connector.IntegrityError:
        print(f"No duplicate entries allowed. Dropping this data... ")
    except mysql.connector.Error as err:
        print(f"Error inserting data: ", err)
    else:
        print("Data successfully inserted into DB!")
