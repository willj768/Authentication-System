import pytest
from auth.auth import register, login
from db_handler import getConnection
from auth.user_lockout import isLocked

@pytest.fixture
def devCreds(monkeypatch):
    monkeypatch.setattr("auth.auth.TEST_MODE", True)
    monkeypatch.setattr("auth.auth.TEST_EMAIL", "dev@example.com")
    monkeypatch.setattr("auth.auth.TEST_PASSWORD", "devpass")

#Correct login details
def testCorrectPassword(user):
    assert login("user@example.com", "password123!") == (True, "Login Successful")

#Incorrect password
def testIncorrectPassword(user):
    assert login("user@example.com", "incorrectpassword") == (False, "Incorrect Details")

#Unregistered email
def testUnknownEmail(user):
    assert login("unknown@example.com", "password123!") == (False, "Incorrect Details")

#Messy email returns true
def testEmailNormalised(user):
    assert login(" USER@Example.com", "password123!") == (True, "Login Successful")

#Login unsuccessful after 3 failed attempts
def testUserLockout(user, clock):
    for _ in range(3):
        login("user@example.com", "incorrectpassword")

    assert login("user@example.com", "password123!") == (False, "Too many attempts. Try again in 5m 0s.")

#User lockout ends after 300 seconds
def testUserLockoutEnds(user, clock):
    for _ in range(3):
        login("user@example.com", "incorrectpassword")

    clock[0] = 1301.0
    assert login("user@example.com", "password123!") == (True, "Login Successful")

#Login success clears failed attempts count
def testSuccessClearsCount(user, clock):
    for _ in range(2):
        login("user@example.com", "incorrectpassword")

    login("user@example.com", "password123!")

    for _ in range(2):
        login("user@example.com", "incorrectpassword")

    assert login("user@example.com", "password123!") == (True, "Login Successful")

def getLogs():
    conn = getConnection()
    rows = conn.execute("SELECT email, result FROM logs").fetchall()
    conn.close()
    return rows

#Correct details logged upon successful login
def testSuccessIncrementsRows(user):
    login("user@example.com", "password123!")
    rows = getLogs()
    assert len(rows) == 1
    assert rows[0]["result"] == "Success"
    assert rows[0]["email"] == "user@example.com"

#Correct details logged upon unsuccessful login
def testFailureIncrementsRows(user):
    login("user@example.com", "incorrectpassword")
    rows = getLogs()
    assert len(rows) == 1
    assert rows[0]["result"] == "Fail"
    assert rows[0]["email"] == "user@example.com"

def testUnknownEmailIncrementsRow(db):
    login("unknown@example.com", "password123!")
    rows = getLogs()
    assert len(rows) == 1
    assert rows[0]["result"] == "Fail"
    assert rows[0]["email"] == "unknown@example.com"

def testLockoutAttemptNotLogged(user, clock):
    for _ in range(3):
        login("user@example.com", "incorrectpassword")
    login("user@example.com", "password123!")
    rows = getLogs()
    assert len(rows) == 3

#Correct details logged upon messy successful login
def testEmailIncrementsRowsNormalised(user):
    login(" USER@Example.com", "password123!")
    rows = getLogs()
    assert len(rows) == 1
    assert rows[0]["email"] == "user@example.com"

def testDevModeOn(devCreds):
    assert login("dev@example.com", "devpass") == (True, "Login successful (test mode)")

def testDevModeOff(db, devCreds, monkeypatch):
    monkeypatch.setattr("auth.auth.TEST_MODE", False)
    assert login("dev@example.com", "devpass") == (False, "Incorrect Details")

def testIncorrectDevPassword(db, devCreds):
    assert login("dev@example.com", "incorrectpassword") == (False, "Incorrect Details")

def testUserLoginWithDevMode(user, devCreds):
    assert login("user@example.com", "password123!") == (True, "Login Successful")

def testDevLoginDB(db, devCreds):
    login("dev@example.com", "devpass")
    rows = getLogs()
    assert len(rows) == 0

def testDevModeIgnoresLockout(db, devCreds, clock):
    for _ in range(3):
        login("dev@example.com", "incorrectpassword")
    clock[0] = 1299.0
    assert isLocked("dev@example.com")[0] is True
    assert login("dev@example.com", "devpass") == (True, "Login successful (test mode)")




