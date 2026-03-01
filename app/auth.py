import bcrypt
import pandas as pd
from datetime import datetime
import random
import string
import time
import re
import os

REGISTER_CSV_NAME = "userdata.csv"
LOGS_CSV_NAME = "logs.csv"
FAILURE_CSV_NAME = "failedattempts.csv"

REGISTER_CSV_PATH = os.path.abspath(REGISTER_CSV_NAME)
LOGS_CSV_PATH = os.path.abspath(LOGS_CSV_NAME)
FAILURE_CSV_PATH = os.path.abspath(FAILURE_CSV_NAME)

WINDOW_SECONDS = 300
MAX_ATTEMPTS = 3

EMAIL_REGEX = r"^[a-zA-Z0-9]+[a-zA-Z0-9._+-]*@[a-zA-Z0-9-]+(\.[a-zA-Z]{2,})+$"

def loadRegisterData():
    return pd.read_csv(REGISTER_CSV_PATH)

def saveRegisterData(dfRegister):
    dfRegister.to_csv(REGISTER_CSV_PATH, index=False)

def loadLogsData():
    return pd.read_csv(LOGS_CSV_PATH)

def saveLogsData(dfLogs):
    dfLogs.to_csv(LOGS_CSV_PATH, index=False)

def loadFailedLogsData():
    return pd.read_csv(FAILURE_CSV_PATH)

def saveFailedLogsData(dfFailedLogs):
    dfFailedLogs.to_csv(FAILURE_CSV_PATH, index=False)

def register(email, password, confirmPassword):

    dfRegister = loadRegisterData()
    email = email.strip().lower()

    if isValidEmail(email) == False:
        return False, "Email not valid"

    if password != confirmPassword:
        return False, "Passwords do not match"

    if (dfRegister["email"].str.lower() == email).any():
        return False, "Email already registered"
    
    if not checkPassword(password):
        return False, "Password does not meet requirements"
    
    hashedPassword = bcrypt.hashpw(
    password.encode('utf-8'),
    bcrypt.gensalt()
    ).decode('utf-8')

    newUser = {
    "email": email,
    "password": hashedPassword,
    "user_created": datetime.now()
    }

    dfRegister.loc[len(dfRegister)] = newUser
    saveRegisterData(dfRegister)

    return True, "Registration Successful"

def login(email, password):

    dfRegister = loadRegisterData()
    email = email.strip().lower()

    now = datetime.now()

    if not (dfRegister["email"].str.lower() == email).any():
        return False, "Email not found"
    
    storedHash = dfRegister.loc[dfRegister["email"] == email, "password"].values[0]
    storedHash = storedHash.encode('utf-8')

    if bcrypt.checkpw(password.encode('utf-8'), storedHash):
            
            locked, minutes, seconds = isLocked(email)

            if locked:
                return False, f"Too many attempts. Try again in {minutes}m {seconds}s."

            loginResult = "Success"
            logUser(email, now, loginResult)

            return True, "Login successful"
    
    loginResult = "Fail"
    logUser(email, now, loginResult)
    
    return False, "Incorrect password"
    
def checkPassword(password):
    SPECIAL_CHAR = "!@#$%^&*()-+?_=,<>/"
    
    hasSpecial = any(c in SPECIAL_CHAR for c in password)
    hasNumber = any(c.isdigit() for c in password)
    hasLetter = any(c.isalpha() for c in password)
    hasLength = len(password) >= 8

    return hasSpecial and hasNumber and hasLetter and hasLength
    
def generateRandomPassword():
    
    letters = string.ascii_letters
    digits = string.digits
    specials = string.punctuation

    password = [random.choice(letters), random.choice(digits), random.choice(specials)]

    allChars = letters + digits + specials
    password += random.choices(allChars, k=9)

    random.shuffle(password)

    return "".join(password)

def logUser(email, now, loginResult):

    dfLogs = loadLogsData()

    newUserLog = {
    "email": email,
    "user_log": now,
    "login_result": loginResult
    }

    dfLogs.loc[len(dfLogs)] = newUserLog

    saveLogsData(dfLogs)

    if loginResult == "Fail":
        logFailedAttempt(email)

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
    
    if attempts >= MAX_ATTEMPTS and timePassed <= WINDOW_SECONDS:
        
        timeRemaining = WINDOW_SECONDS - timePassed

        minutes = round(timeRemaining // 60)
        seconds = round(timeRemaining % 60)

        return True, minutes, seconds

    
    return False, 0, 0

def isValidEmail(email):
    return re.match(EMAIL_REGEX, email) is not None
    

