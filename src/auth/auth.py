import bcrypt
from datetime import datetime
from .db_handler import loadRegisterData, saveRegisterData
from .data_validation import isValidEmail, checkPassword
from .user_lockout import isLocked, resetFailedAttempts, logFailedAttempt
from .logger import logUser
from .config import TEST_MODE, TEST_EMAIL, TEST_PASSWORD

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

    overrideResult = overrideLogin(email, password)
    if overrideResult:
        return overrideResult

    dfRegister = loadRegisterData()
    email = email.strip().lower()

    now = datetime.now()

    if not (dfRegister["email"].str.lower() == email).any():
        return False, "Email not found"
    
    storedHash = dfRegister.loc[dfRegister["email"] == email, "password"].values[0]
    storedHash = storedHash.encode('utf-8')

    locked, minutes, seconds = isLocked(email)

    if locked:
        return False, f"Too many attempts. Try again in {minutes}m {seconds}s."

    if bcrypt.checkpw(password.encode('utf-8'), storedHash):

            loginResult = "Success"
            logUser(email, now, loginResult)
            resetFailedAttempts(email)

            return True, "Login successful"
    else:
        loginResult = "Fail"
        logUser(email, now, loginResult)
        logFailedAttempt(email)
    
        return False, "Incorrect password"

def overrideLogin(email, password):
    if not TEST_MODE:
        return None

    email = email.strip().lower()
    password = password.strip()

    if email == TEST_EMAIL and password == TEST_PASSWORD:
        return True, "Login successful (test mode)"

    return None
