from auth.data_validation import isValidEmail, checkPassword
import pytest

@pytest.mark.parametrize("email, expected", [
    ("user@example.com", True), #Valid email
    ("user-example.com", False), #No @
    ("user@example", False), #No domain extension
    ("", False), #Empty string
    ("user @example.com", False), #Spaces
    ("!user@example.com", False), #Start with symbol
])

def testEmailValidation(email, expected):
    assert isValidEmail(email) == expected

@pytest.mark.parametrize("password, expected", [
    ("password123!", True), #Valid password
    ("password!", False), #No number
    ("12345678!", False), #No letter
    ("password123", False), #No special char
    ("aaa123!", False), #Too short
    ("a1!" + "x" * 70, False), #Too long
    ("aaaaaa1!", True), #Exact min length
    ("a1!" + "x" * 69, True), #Exact max length
])

def testCheckPassword(password, expected):
    assert checkPassword(password) == expected