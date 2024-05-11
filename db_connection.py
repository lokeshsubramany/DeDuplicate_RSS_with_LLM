import sqlite3

db_name = 'RssFeeds.db'

def get_connection():
    """
    Establish a connection to a SQLite database.
    
    Args:
        db_name (str): Name of the SQLite database file.
    
    Returns:
        sqlite3.Connection: Connection object to the SQLite database.
    """
    try:
        con = sqlite3.connect(db_name)
        return con
    except sqlite3.Error as e:
        print("Error connecting to database: ", e)
        return None

def create_db():
    """
    Create a new SQLite database and execute the given query to create tables.
    
    Args:
        db_name (str): Name of the SQLite database file.
        query (str): SQL query to create tables in the database.
    
    Returns:
        sqlite3.Connection: Connection object to the SQLite database.
    """
    
    query = ["CREATE TABLE IF NOT EXISTS FEEDS( Feedname, Article_title UNIQUE, Article_URL, Duplicate, Fetch_Date, Summary)",
    "CREATE TABLE IF NOT EXISTS SUMMARY( Feedname, Article_URL,Summary)"]

    con = get_connection()
    
    if con is None:
        return None
    
    try:
        for item in query:
            cur = con.cursor()
            cur.execute(item)
            con.commit()
        #return con
    except sqlite3.Error as e:
        print("Error creating database: ", e)
        con.close()
        #return None
    
    print("DB created successfully")

def insert_to_db(data, query):
    """
    Insert data into SQLite database using executemany.
    
    Args:
        con (sqlite3.Connection): Connection object to the SQLite database.
        data (list of tuples): Data to be inserted into the database.
        query (str): SQL query for insertion.
    
    Returns:
        None
    """
    con = get_connection()

    if not data:
        print("No data to insert.")
        return
    
    try:
        cur = con.cursor()
        cur.executemany(query, data)
        con.commit()
    except sqlite3.Error as e:
        print("Error inserting data into database: ", e)
        con.rollback()

def insert_to_FEEDS(data):
    con = get_connection()

    if len(data) == 0:
        print("No data to insert.")
        return
    
    try:
        cur = con.cursor()

        query = "INSERT OR REPLACE INTO FEEDS(Article_title,Article_URL,Feedname,Fetch_Date) VALUES (?, ?, ?, ?)"

        cur.executemany(query, data)
        con.commit()
        con.close()
    except sqlite3.Error as e:
        print("Error inserting data into database: ", e)
        con.rollback()
        con.close()

def insert_to_FEEDS_with_summary(data):
    con = get_connection()

    if len(data) == 0:
        print("No data to insert.")
        return
    
    try:
        cur = con.cursor()

        query = "INSERT OR REPLACE INTO FEEDS(Feedname, Article_title,Article_URL,Duplicate,Fetch_Date,Summary) VALUES (?, ?, ?, ?, ?, ?)"

        cur.executemany(query, data)
        con.commit()
        con.close()
    except sqlite3.Error as e:
        print("Error inserting data into database: ", e)
        con.rollback()
        con.close()

def insert_to_Summary(data):
    con = get_connection()

    if len(data) == 0:
        print("No data to insert.")
        return
    
    try:
        cur = con.cursor()

        query = "INSERT OR REPLACE INTO SUMMARY(Feedname, Article_URL,Summary) VALUES (?, ?, ?)"

        cur.executemany(query, data)
        con.commit()
        con.close()
    except sqlite3.Error as e:
        print("Error inserting data into database: ", e)
        con.rollback()
        con.close()


def delete_from_db(tablename):
    """
    Delete data from SQLite database.
    
    Args:
        con (sqlite3.Connection): Connection object to the SQLite database.
        query (str): SQL query for deletion.
    
    Returns:
        None
    """
    con = get_connection()
    query = "DROP TABLE IF EXISTS " + tablename
    try:
        cur = con.cursor()
        cur.execute(query)
        con.commit()
    except sqlite3.Error as e:
        print("Error deleting data from database: ", e)
        con.rollback()


def query_db(query):
    """
    Execute a SQL query and fetch results from SQLite database.
    
    Args:
        con (sqlite3.Connection): Connection object to the SQLite database.
        query (str): SQL query to be executed.
    
    Returns:
        list of tuples: Result set fetched from the database.
    """
    con = get_connection()

    try:
        cur = con.cursor()
        cur.execute(query)
        return cur.fetchall()
    except sqlite3.Error as e:
        print("Error executing query: ", e)
        return []
    