import bcrypt
from datetime import datetime
from db_handler import saveRegisterData, getRegisterEmail, getPassword
from .data_validation import isValidEmail, checkPassword
from .user_lockout import isLocked, resetFailedAttempts, logFailedAttempt
from .logger import logUser
from config import TEST_MODE, TEST_EMAIL, TEST_PASSWORD, TIMEZONE

def register(email, password, confirmPassword):
    """
    Register a new account

    Args:
        email (str): The user's email address
        password (str): The user's password
        confirmPassword (str): Must match password

    Returns:
        tuple (success (boolean), message (str))
    """

    email = email.strip().lower()

    if isValidEmail(email) == False:
        return False, "Email not valid"

    if password != confirmPassword:
        return False, "Passwords do not match"

    #Ensures email is not already in database
    if getRegisterEmail(email):
        return False, "Email already registered"
    
    if not checkPassword(password):
        return False, "Password does not meet requirements"
    
    #Hash password and add salt before storing
    hashedPassword = bcrypt.hashpw(
    password.encode('utf-8'),
    bcrypt.gensalt()
    ).decode('utf-8')

    newUser = {
    "email": email,
    "password": hashedPassword,
    "user_created": datetime.now(TIMEZONE)
    }

    saveRegisterData(newUser)

    return True, "Registration Successful"

def login(email, password):

    """
    Login to existing account

    Args:
        email (str): The user's email address
        password (str): Desired password

    Returns:
        tuple (success (boolean), message (str))
    """

    email = email.strip().lower()

    overrideResult = overrideLogin(email, password)
    if overrideResult:
        return overrideResult

    now = datetime.now(TIMEZONE)

    locked, minutes, seconds = isLocked(email)

    if locked:
        return False, f"Too many attempts. Try again in {minutes}m {seconds}s."

    #Takes hashed password which corresponds with given email    
    storedHash = getPassword(email)

    if storedHash is None:
        bcrypt.checkpw(password.encode('utf-8'), bcrypt.hashpw(b"dummy", bcrypt.gensalt()))
        loginResult = "Fail"
        logUser(email, now, loginResult)
        logFailedAttempt(email)
        return False, "Incorrect Details"

    storedHash = storedHash.encode('utf-8')

    #Password authentication
    if bcrypt.checkpw(password.encode('utf-8'), storedHash):
            loginResult = "Success"
            logUser(email, now, loginResult)
            resetFailedAttempts(email)
            return True, "Login Successful"
    else:
        loginResult = "Fail"
        logUser(email, now, loginResult)
        logFailedAttempt(email)
        return False, "Incorrect Details"

def overrideLogin(email, password):
    """
    Allows developer to bypass login logic using hardcoded credentials

    Args:
        email (str): The email provided by the user
        password (str): The password provided by the user

    Returns:
        tuple (True, success message): If test credentials match
        None: If not in test mode or credentials don't match
    """

    if not TEST_MODE:
        return None

    password = password.strip()

    if email == TEST_EMAIL and password == TEST_PASSWORD:
        return True, "Login successful (test mode)"

    return None
