import sqlite3
import pandas as pd
from .config import DB_PATH

def getConnection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initDB():
    conn = getConnection()
    cursor = conn.cursor()

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
    """)

    conn.commit()
    conn.close()

def loadRegisterData():
    conn = getConnection()
    df = pd.read_sql_query("SELECT * FROM users", conn)
    conn.close()
    return df

def saveRegisterData(dfRegister):
    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (email, password, user_created) VALUES (?, ?, ?)",
        (dfRegister.iloc[-1]["email"],
         dfRegister.iloc[-1]["password"],
         str(dfRegister.iloc[-1]["user_created"]))
    )

    conn.commit()
    conn.close()

def loadLogsData():
    conn = getConnection()
    df = pd.read_sql_query("SELECT * FROM logs", conn)
    conn.close()
    return df

def saveLogsData(dfLogs):
    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO logs (email, timestamp, result) VALUES (?, ?, ?)",
        (dfLogs.iloc[-1]["email"],
         str(dfLogs.iloc[-1]["timestamp"]),
         dfLogs.iloc[-1]["result"])
    )

    conn.commit()
    conn.close()

def loadFailedLogsData():
    conn = getConnection()
    df = pd.read_sql_query("SELECT * FROM failed_attempts", conn)
    conn.close()
    return df

def saveFailedLogsData(dfFailedLogs):
    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM failed_attempts", )
    
    if not dfFailedLogs.empty:
        dfFailedLogs.to_sql("failed_attempts", conn, if_exists="append", index=False)

    conn.commit()
    conn.close()