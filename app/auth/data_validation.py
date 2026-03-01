import re
from .config import EMAIL_REGEX

def checkPassword(password):
    SPECIAL_CHAR = "!@#$%^&*()-+?_=,<>/"
    
    hasSpecial = any(c in SPECIAL_CHAR for c in password)
    hasNumber = any(c.isdigit() for c in password)
    hasLetter = any(c.isalpha() for c in password)
    hasLength = len(password) >= 8

    return hasSpecial and hasNumber and hasLetter and hasLength

def isValidEmail(email):
    return re.match(EMAIL_REGEX, email) is not None