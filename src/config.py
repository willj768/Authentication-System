from pathlib import Path
import os
from dotenv import load_dotenv
import pytz

#Establishes path to database
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "auth.db"

ALLOWED_ORIGINS = ["http://localhost:5000", "http://192.168.68.128:5000"]

WINDOW_SECONDS = 300 #Lockout time after 3 failed attempts
MAX_ATTEMPTS = 3 #Lockout after this many attempts

EMAIL_REGEX = r"^[a-zA-Z0-9]+[a-zA-Z0-9._+-]*@[a-zA-Z0-9-]+(\.[a-zA-Z]{2,})+$" #Ensures emails are formatted correctly

#Test environment

load_dotenv()

TEST_MODE = os.getenv("TEST_MODE", "False") == "True"
TEST_EMAIL = os.getenv("TEST_EMAIL")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")

SECRET_KEY = os.getenv("SECRET_KEY")

#Chat Application
MESSAGE_HISTORY_LIMIT = 50

#Current time in UK
TIMEZONE = pytz.timezone("Europe/London")

#App
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(PROJECT_ROOT, "templates")
STATIC_DIR = os.path.join(PROJECT_ROOT, "static")

SESSION_COOKIE_SAMESITE = "Strict"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False
