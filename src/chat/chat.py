import sqlite3
from auth.config import DB_PATH, MESSAGE_HISTORY_LIMIT
from auth.db_handler import getConnection, initDB

def sendMessage(email, message):

    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO messages (email, message) VALUES (?, ?)",
        (email, message)
    )

    conn.commit()
    conn.close()

def getRecentMessages(limit=MESSAGE_HISTORY_LIMIT):
    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT email, message, timestamp FROM messages ORDER BY timestamp DESC LIMIT ?",
        (limit,)
    )

    messages = cursor.fetchall()
    conn.close()

    return [{"email": row[0], "message": row[1], "timestamp": row[2]} for row in reversed(messages)]

