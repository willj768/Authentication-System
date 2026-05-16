import time
from .config import WINDOW_SECONDS, MAX_ATTEMPTS
from .db_handler import saveFailedLogsData, getFailedLog, getFirstAttempt, getAttemptNum, removeFailedLog
import traceback

def logFailedAttempt(email):

    """
    Records a failed authentication attempt and tracks consecutive failures

    Args:
        email (str): The user's email address
    """

    email = email.lower()
    now = time.time() #unix timestamp

    #Checks for other failed attempts from the given email
    if getFailedLog(email):
       
        firstTime = getFirstAttempt(email)
        timePassed = now - float(firstTime)
        numAttempts = getAttemptNum(email)

        newFailedLog = {
            "email": email,
            "attempt_failed": numAttempts,
            "first_attempt_time": firstTime
        }

        #Resets counter if first attempt time is missing or lockout window has expired
        if getFirstAttempt(email) is None or timePassed > WINDOW_SECONDS:
            newFailedLog["attempt_failed"] = 1
            newFailedLog["first_attempt_time"] = now
        else:
            #If the window is still active then increment the failure counter
            newFailedLog["attempt_failed"] = numAttempts + 1
    else:
        #Creates new entry if the email is not previously recorded
        newFailedLog = {
            "email": email,
            "attempt_failed": 1,
            "first_attempt_time": now
        }
    
    saveFailedLogsData(newFailedLog)

def isLocked(email):
    """
    Checks whether a user is currently locked out due to too many failed attempts, automatically clears the record if the lockout window has expired.

    Args:
        email (str): The user's email address

    Returns:
        tuple: (is_locked: bool, minutes_remaining: int, seconds_remaining: int): Minutes and seconds are 0 if the account is not locked
    """

    email = email.lower()
    now = time.time()

    #If no record is found then account is not locked
    if not getFailedLog(email):
        return False, 0, 0
    
    attempts = getAttemptNum(email)
    firstTime = getFirstAttempt(email)

    #If no timestamp is recorded then account is not locked
    if getFirstAttempt(email) is None:
        return False, 0, 0
    
    timePassed = now - float(firstTime)
    
    #Once the lockout window has expired it is cleared and the account is unlocked
    if timePassed > WINDOW_SECONDS:
        removeFailedLog(email)
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

    email = email.lower()

    # Clear the attempt count and timestamp if a record exists
    if getFailedLog(email):
        removeFailedLog()