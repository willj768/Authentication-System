from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

REGISTER_CSV_PATH = DATA_DIR / "userdata.csv"
LOGS_CSV_PATH = DATA_DIR / "logs.csv"
FAILURE_CSV_PATH = DATA_DIR / "failedattempts.csv"

WINDOW_SECONDS = 300
MAX_ATTEMPTS = 3

EMAIL_REGEX = r"^[a-zA-Z0-9]+[a-zA-Z0-9._+-]*@[a-zA-Z0-9-]+(\.[a-zA-Z]{2,})+$"