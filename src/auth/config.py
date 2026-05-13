from pathlib import Path

#Establishes path to database
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "auth.db"

WINDOW_SECONDS = 300 #Lockout time after 3 failed attempts
MAX_ATTEMPTS = 3 #Lockout after this many attempts

EMAIL_REGEX = r"^[a-zA-Z0-9]+[a-zA-Z0-9._+-]*@[a-zA-Z0-9-]+(\.[a-zA-Z]{2,})+$" #Ensures emails are formatted correctly

#Test environment
TEST_MODE = True
TEST_EMAIL = "test"
TEST_PASSWORD = "test"