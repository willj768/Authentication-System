import time
import pandas as pd
from .config import WINDOW_SECONDS, MAX_ATTEMPTS
from .csv_handler import loadFailedLogsData, saveFailedLogsData
import traceback

def logFailedAttempt(email):

    dfFailedLogs = loadFailedLogsData()
    email = email.lower()
    now = time.time()

    mask = dfFailedLogs["email"].str.lower() == email

    if mask.any():
       
        firstTime = dfFailedLogs.loc[mask, "first_attempt_time"].values[0]
        timePassed = now - float(firstTime)

        if pd.isna(firstTime) or timePassed > WINDOW_SECONDS:
            dfFailedLogs.loc[mask, "attempt_failed"] = 1
            dfFailedLogs.loc[mask, "first_attempt_time"] = now
        else:
            dfFailedLogs.loc[mask, "attempt_failed"] += 1
    else:
        newFailedLog = {
            "email": email,
            "attempt_failed": 1,
            "first_attempt_time": now
        }

        dfFailedLogs.loc[len(dfFailedLogs)] = newFailedLog
    
    saveFailedLogsData(dfFailedLogs)

def isLocked(email):

    dfFailedLogs = loadFailedLogsData()
    email = email.lower()
    now = time.time()

    mask = dfFailedLogs["email"].str.lower() == email

    if not mask.any():
        return False, 0, 0
    
    attempts = dfFailedLogs.loc[mask, "attempt_failed"].values[0]
    firstTime = dfFailedLogs.loc[mask, "first_attempt_time"].values[0]

    if pd.isna(firstTime):
        return False, 0, 0
    
    timePassed = now - float(firstTime)
    
    if timePassed > WINDOW_SECONDS:
        dfFailedLogs = dfFailedLogs[~mask]
        saveFailedLogsData(dfFailedLogs)
        return False, 0, 0

    if attempts >= MAX_ATTEMPTS:
        
        timeRemaining = WINDOW_SECONDS - timePassed

        minutes = round(timeRemaining // 60)
        seconds = round(timeRemaining % 60)

        return True, minutes, seconds
    
    if timePassed > WINDOW_SECONDS:
        dfFailedLogs.loc[mask, "attempt_failed"] = 0
        dfFailedLogs.loc[mask, "first_attempt_time"] = None
        saveFailedLogsData(dfFailedLogs)
    
    return False, 0, 0

def resetFailedAttempts(email):
    dfFailedLogs = loadFailedLogsData()
    email = email.lower()

    mask = dfFailedLogs["email"].str.lower() == email

    if mask.any():
        dfFailedLogs.loc[mask, "attempt_failed"] = 0
        dfFailedLogs.loc[mask, "first_attempt_time"] = None
        saveFailedLogsData(dfFailedLogs)