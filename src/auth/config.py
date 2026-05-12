from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

REGISTER_CSV_PATH = DATA_DIR / "userdata.csv"
LOGS_CSV_PATH = DATA_DIR / "logs.csv"
FAILURE_CSV_PATH = DATA_DIR / "failedattempts.csv"

DB_PATH = DATA_DIR / "auth.db"

#Adjust to 300 after testing
WINDOW_SECONDS = 10
MAX_ATTEMPTS = 3

EMAIL_REGEX = r"^[a-zA-Z0-9]+[a-zA-Z0-9._+-]*@[a-zA-Z0-9-]+(\.[a-zA-Z]{2,})+$"

TEST_MODE = True
TEST_EMAIL = "test"
TEST_PASSWORD = "test"