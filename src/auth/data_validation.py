import re
from .config import EMAIL_REGEX

def checkPassword(password):

    """
    Compares given password to password rules

    Args:
        password (str): Given password from register

    Returns:
        hasSpecial (boolean): Checks for special character
        hasNumber (boolean): Checks for number
        hasLetter (boolean): Checks for letter
        hasLength (boolean): Checks password length
    """

    SPECIAL_CHAR = "!@#$%^&*()-+?_=,<>/"
    
    hasSpecial = any(c in SPECIAL_CHAR for c in password)
    hasNumber = any(c.isdigit() for c in password)
    hasLetter = any(c.isalpha() for c in password)
    hasLength = len(password) >= 8

    return hasSpecial and hasNumber and hasLetter and hasLength

def isValidEmail(email):
    #Returns whether email is in the correct format
    return re.match(EMAIL_REGEX, email) is not None