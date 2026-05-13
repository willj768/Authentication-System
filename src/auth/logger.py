from .db_handler import loadLogsData, saveLogsData
from .user_lockout import logFailedAttempt

def logUser(email, now, loginResult):

    """
    Logs all login attempts

    Args:
        email (str): The user's email
        now (datetime): The timestamp of the login attempt
        loginResult (boolean): Whether the attempt was successful or failed
    """

    dfLogs = loadLogsData()

    newUserLog = {
    "email": email,
    "timestamp": now,
    "result": loginResult
    }

    dfLogs.loc[len(dfLogs)] = newUserLog

    saveLogsData(dfLogs)