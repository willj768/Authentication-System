import pandas as pd
from .config import REGISTER_CSV_PATH, LOGS_CSV_PATH, FAILURE_CSV_PATH

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