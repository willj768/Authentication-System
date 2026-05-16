from .db_handler import saveMessage, getRecentMessages
from .config import MESSAGE_HISTORY_LIMIT

def sendMessage(email, message):
    saveMessage(email, message)

def loadHistory():
    messages = getRecentMessages(limit=MESSAGE_HISTORY_LIMIT)
    return messages
