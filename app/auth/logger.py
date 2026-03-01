from .csv_handler import loadLogsData, saveLogsData
from .user_lockout import logFailedAttempt

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