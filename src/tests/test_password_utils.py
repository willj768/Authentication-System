from auth.password_utils import generateRandomPassword
from auth.data_validation import checkPassword

def testRandomPasswords():
    for _ in range(200):
        password = generateRandomPassword()

        assert checkPassword(password) == True
        assert len(password) == 12