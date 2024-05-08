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
    
    query = "CREATE TABLE IF NOT EXISTS FEEDS( Feedname, Article_title UNIQUE, Article_URL, Duplicate, Date, Summary)"    

    con = get_connection(db_name)
    if con is None:
        return None
    
    try:
        cur = con.cursor()
        cur.execute(query)
        con.commit()
        return con
    except sqlite3.Error as e:
        print("Error creating database: ", e)
        con.close()
        return None

def insert_to_db(con, table, data, query):
    """
    Insert data into SQLite database using executemany.
    
    Args:
        con (sqlite3.Connection): Connection object to the SQLite database.
        data (list of tuples): Data to be inserted into the database.
        query (str): SQL query for insertion.
    
    Returns:
        None
    """
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

def delete_from_db(con, query):
    """
    Delete data from SQLite database.
    
    Args:
        con (sqlite3.Connection): Connection object to the SQLite database.
        query (str): SQL query for deletion.
    
    Returns:
        None
    """
    try:
        cur = con.cursor()
        cur.execute(query)
        con.commit()
    except sqlite3.Error as e:
        print("Error deleting data from database: ", e)
        con.rollback()


def query_db(con, query):
    """
    Execute a SQL query and fetch results from SQLite database.
    
    Args:
        con (sqlite3.Connection): Connection object to the SQLite database.
        query (str): SQL query to be executed.
    
    Returns:
        list of tuples: Result set fetched from the database.
    """
    try:
        cur = con.cursor()
        cur.execute(query)
        return cur.fetchall()
    except sqlite3.Error as e:
        print("Error executing query: ", e)
        return []