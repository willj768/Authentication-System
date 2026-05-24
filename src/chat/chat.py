import sqlite3
from auth.config import DB_PATH, MESSAGE_HISTORY_LIMIT
from auth.db_handler import getConnection, initDB

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

