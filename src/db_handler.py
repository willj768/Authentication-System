import sqlite3
from config import DB_PATH, MESSAGE_HISTORY_LIMIT

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

    """Initialises the database by creating required tables if they do not already exist"""

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

    """
    Saves user data into the users table

    Args:
        newUser (dict): Stores the email, hashed password, and timestamp
    """

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

    """
    Checks if an email has already been registered
    
    Args:
        email (str): The email given by the user

    Returns:
        True: If the email is already in the database
        False: If the email is not in the database
    """

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

    """
    Gets the password for the given email

    Args:
        email (str): The email given by the user
    
    Returns:
        result[0] (str): The password which matches the email
        None: If the email does not exist or the password corresponding to the given email is not found
    """


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

    """
    Saves new logs to the logs table

    Args:
        newUserLog (dict): Stores the email, timestamp, and result of a log (success or fail)
    """

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

    """
    Saves a failed attempt into the failed_attempts table. If the email already exists in the table then the attempt_failed value is incremented.

    Args:
        newFailedLog (dict): Stores the email, attempt number failed, and first attempt time
    """

    conn = getConnection()
    cursor = conn.cursor()

    if getFailedLog(newFailedLog["email"]): #Checks if the email given already exists in the failed attempt table
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

    """
    Checks if the email given is currently the failed_attempts table

    Args:
        email (str): The email given by the user

    Returns:
        True: If the email given is in the failed_attempts table
        False: If the email given is not in the failed_attempts table
    """

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

    """
    Gets the time of the first failed attempt from the failed_attempts table

    Args:
        email (str): The email given by the user

    Returns:
        result[0] (str): The first failed attempt time
        None: If there is no first failed attempt time
    """

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

    """
    Gets the number of failed attempts from the failed_attempts table

    Args:
        email (str): The email given by the user
    
    Returns:
        result[0] (int): The number of previous attempts failed
        None: If there are no previous failed attempts
    """

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

    """
    Removes failed login attempts if the lockout window has passed or the correct password is given

    Args:
        email (str): The email given by the user
    """
    
    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM failed_attempts WHERE email = ?",
        (email,)
    )

    conn.commit()
    conn.close()

def clearLogs(cursor):

    """
    Clears logs from the logs table if they are over 30 days old
    
    Args:
        cursor (sqlite3.cursor): Active cursor from the calling function
    """
    
    cursor.execute(
        "DELETE FROM logs WHERE timestamp < datetime('now', '-30 days')",
    )

def sendMessage(email, message):

    """
    When the server receives a message it is added to the messages table

    Args:
        email (str): The email of the sender
        message (str): The content of the message
    """

    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO messages (email, message) VALUES (?, ?)",
        (email, message)
    )

    conn.commit()
    conn.close()

def getRecentMessages(limit=MESSAGE_HISTORY_LIMIT):

    """
    Collects message history when a new user connects

    Args:
        limit (int): The max number of messages retrieved

    Returns:
        list[dict]: A list of messages in chronological order, containing the sender's email, the message content, and the timestamp
    """


    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT email, message, timestamp FROM messages ORDER BY timestamp DESC LIMIT ?",
        (limit,)
    )

    messages = cursor.fetchall()
    conn.close()

    return [{"email": row[0], "message": row[1], "timestamp": row[2]} for row in reversed(messages)]
