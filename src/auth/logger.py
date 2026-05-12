from .db_handler import loadLogsData, saveLogsData
from .user_lockout import logFailedAttempt

def logUser(email, now, loginResult):

    dfLogs = loadLogsData()

    newUserLog = {
    "email": email,
    "timestamp": now,
    "result": loginResult
    }

    dfLogs.loc[len(dfLogs)] = newUserLog

    saveLogsData(dfLogs)