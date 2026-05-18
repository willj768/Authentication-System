from pathlib import Path
import os
from dotenv import load_dotenv
import pytz

#Establishes path to database
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "auth.db"

WINDOW_SECONDS = 300 #Lockout time after 3 failed attempts
MAX_ATTEMPTS = 3 #Lockout after this many attempts

EMAIL_REGEX = r"^[a-zA-Z0-9]+[a-zA-Z0-9._+-]*@[a-zA-Z0-9-]+(\.[a-zA-Z]{2,})+$" #Ensures emails are formatted correctly

#Test environment

load_dotenv()

TEST_MODE = os.getenv("TEST_MODE", "False") == "True"
TEST_EMAIL = os.getenv("TEST_EMAIL")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")

#Chat Application
MESSAGE_HISTORY_LIMIT = 50

#Current time in UK
TIMEZONE = pytz.timezone("Europe/London")
