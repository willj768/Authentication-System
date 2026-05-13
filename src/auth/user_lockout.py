import time
import pandas as pd
from .config import WINDOW_SECONDS, MAX_ATTEMPTS
from .db_handler import loadFailedLogsData, saveFailedLogsData
import traceback

def logFailedAttempt(email):

    """
    Records a failed authentication attempt and tracks consecutive failures

    Args:
        email (str): The user's email address
    """

    dfFailedLogs = loadFailedLogsData()
    email = email.lower()
    now = time.time() #unix timestamp

    #Checks for other failed attempts from the given email
    mask = dfFailedLogs["email"].str.lower() == email

    if mask.any():
       
        firstTime = dfFailedLogs.loc[mask, "first_attempt_time"].values[0]
        timePassed = now - float(firstTime)

        #Resets counter if first attempt time is missing or lockout window has expired
        if pd.isna(firstTime) or timePassed > WINDOW_SECONDS:
            dfFailedLogs.loc[mask, "attempt_failed"] = 1
            dfFailedLogs.loc[mask, "first_attempt_time"] = now
        else:
            #If the window is still active then increment the failure counter
            dfFailedLogs.loc[mask, "attempt_failed"] += 1
    else:
        #Creates new entry if the email is not previously recorded
        newFailedLog = {
            "email": email,
            "attempt_failed": 1,
            "first_attempt_time": now
        }

        dfFailedLogs.loc[len(dfFailedLogs)] = newFailedLog
    
    saveFailedLogsData(dfFailedLogs)

def isLocked(email):
    """
    Checks whether a user is currently locked out due to too many failed attempts, automatically clears the record if the lockout window has expired.

    Args:
        email (str): The user's email address

    Returns:
        tuple: (is_locked: bool, minutes_remaining: int, seconds_remaining: int): Minutes and seconds are 0 if the account is not locked
    """
    dfFailedLogs = loadFailedLogsData()
    email = email.lower()
    now = time.time()

    mask = dfFailedLogs["email"].str.lower() == email

    #If no record is found then account is not locked
    if not mask.any():
        return False, 0, 0
    
    attempts = dfFailedLogs.loc[mask, "attempt_failed"].values[0]
    firstTime = dfFailedLogs.loc[mask, "first_attempt_time"].values[0]

    #If no timestamp is recorded then account is not locked
    if pd.isna(firstTime):
        return False, 0, 0
    
    timePassed = now - float(firstTime)
    
    #Once the lockout window has expired it is cleared and the account is unlocked
    if timePassed > WINDOW_SECONDS:
        dfFailedLogs = dfFailedLogs[~mask]
        saveFailedLogsData(dfFailedLogs)
        return False, 0, 0

    #Calculates lockout time remaining if failure threshold is released
    if attempts >= MAX_ATTEMPTS:
        timeRemaining = WINDOW_SECONDS - timePassed

        minutes = round(timeRemaining // 60)
        seconds = round(timeRemaining % 60)

        return True, minutes, seconds
    
    return False, 0, 0

def resetFailedAttempts(email):
    """
    Resets the failed attempt counter for a given email after a successful login

    Args:
        email (str): The user's email address
    """
    dfFailedLogs = loadFailedLogsData()
    email = email.lower()

    mask = dfFailedLogs["email"].str.lower() == email

    # Clear the attempt count and timestamp if a record exists
    if mask.any():
        dfFailedLogs.loc[mask, "attempt_failed"] = 0
        dfFailedLogs.loc[mask, "first_attempt_time"] = None
        saveFailedLogsData(dfFailedLogs)