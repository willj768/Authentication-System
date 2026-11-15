from auth.auth import register
from db_handler import getRegisterEmail, getPassword
import pytest
import bcrypt


def testRegisterSavesUser(db):

    result = register("user@example.com", "password123!", "password123!")
    assert result == (True, "Registration Successful")
    assert getRegisterEmail("user@example.com") is True

def testDatabaseStartsEmpty(db):
    assert getRegisterEmail("user@example.com") is False

@pytest.mark.parametrize("email, password, confirm, expected", [
    ("invalid-email", "password123!", "password123!", "Email not valid"), #Invalid email
    ("user@example.com", "password123!", "password12!", "Passwords do not match"), #Unmatching passwords
    ("user@example.com", "password", "password", "Password does not meet requirements"), #Weak password
])

def testRegisterFailures(db, email, password, confirm, expected):
    result = register(email, password, confirm)
    assert result == (False, expected)

def testRegisterDuplicateEmail(db):
    register("user@example.com", "password123!", "password123!")
    result = register("user@example.com", "password123!", "password123!")
    assert result == (False, "Email already registered")

def testRegisterNormalisesEmail(db):
    register(" USER@Example.com", "password123!", "password123!")
    assert getRegisterEmail("user@example.com") is True
    assert getRegisterEmail(" USER@Example.com") is False

def testPasswordHashed(db):
    register("user@example.com", "password123!", "password123!")
    password = getPassword("user@example.com")
    assert password != "password123!"
    assert password.startswith("$2b$")
    assert bcrypt.checkpw(b"password123!", password.encode("utf-8")) is True



