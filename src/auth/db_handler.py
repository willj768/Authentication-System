import sqlite3
from .config import DB_PATH

def getConnection():

    """
    Creates and returns a connection to the SQLite database

    Returns:
        sqlite3.Connection: Active database connection
    """

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row #Allows results to be accessed by column name rather than index
    return conn

def initDB():

    #Initialises the database by creating required tables if they do not already exist

    conn = getConnection()
    cursor = conn.cursor() #Allows SQL commands to be run

    """
    users - Stores registered accounts
    logs - Tracks all login attempts
    failed_attempts - Tracks consecutive failures for each email
    """

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            user_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            result TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS failed_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            attempt_failed INTEGER DEFAULT 0,
            first_attempt_time REAL
        );

        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()

def saveRegisterData(newUser):

    #Saves user data into the user table

    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (email, password, user_created) VALUES (?, ?, ?)",
        (newUser["email"],
         newUser["password"],
         str(newUser["user_created"]))
    )

    conn.commit()
    conn.close()

def getRegisterEmail(email):

    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT email FROM users WHERE email = ?",
        (email,)
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None

def getPassword(email):

    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE email = ?",
        (email,)
    )

    result = cursor.fetchone()

    conn.close()

    return result[0] if result is not None else None

def saveLogsData(newUserLog):

    #Saves log data into the logs table

    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO logs (email, timestamp, result) VALUES (?, ?, ?)",
        (newUserLog["email"],
         newUserLog["timestamp"],
         newUserLog["result"])
    )

    clearLogs(cursor)

    conn.commit()
    conn.close()

def saveFailedLogsData(newFailedLog):

    conn = getConnection()
    cursor = conn.cursor()

    if getFailedLog(newFailedLog["email"]):
        cursor.execute(
            "UPDATE failed_attempts SET attempt_failed = ?, first_attempt_time = ? WHERE email = ?",
            (newFailedLog["attempt_failed"],
             newFailedLog["first_attempt_time"],
             newFailedLog["email"])
        )
    else:
        cursor.execute(
            "INSERT INTO failed_attempts (email, attempt_failed, first_attempt_time) VALUES (?, ?, ?)",
            (newFailedLog["email"],
             newFailedLog["attempt_failed"],
             newFailedLog["first_attempt_time"])
        )

    conn.commit()
    conn.close()

def getFailedLog(email):

    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT email FROM failed_attempts WHERE email = ?",
        (email,)
    )

    result = cursor.fetchone()
    
    conn.close()

    return result is not None

def getFirstAttempt(email):

    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT first_attempt_time FROM failed_attempts WHERE email = ?",
        (email,)
    )

    result = cursor.fetchone()

    conn.close()

    return result[0] if result is not None else None

def getAttemptNum(email):

    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT attempt_failed FROM failed_attempts WHERE email = ?",
        (email,)
    )

    result = cursor.fetchone()

    conn.close()

    return result[0] if result is not None else None

def removeFailedLog(email):
    
    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM failed_attempts WHERE email = ?",
        (email,)
    )

    conn.commit()
    conn.close()

def clearLogs(cursor):
    
    cursor.execute(
        "DELETE FROM logs WHERE timestamp < datetime('now', '-30 days')",
    )
