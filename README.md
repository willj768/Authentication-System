# Authentication System
A full-featured web-based authentication system built with Flask, featuring user registration, secure login, password hashing, and account lockout protection.

## Features

### 🔐 Security
- **Bcrypt Password Hashing**: Passwords are securely hashed using bcrypt with salt generation
- **Password Strength Validation**: Enforces strong passwords requiring:
  - Minimum 8 characters
  - At least one special character (!@#$%^&*()-+?_=,<>/)
  - At least one number
  - At least one letter
- **Account Lockout Protection**: Implements rate limiting with automatic lockout after 3 failed login attempts within a 5-minute window
- **Email Validation**: Validates email format using regex pattern matching

### 👤 User Management
- **User Registration**: Create new accounts with email and password
- **User Login**: Secure login with password verification
- **Password Generation**: Auto-generate strong random passwords
- **Login Logging**: Track all login attempts (success and failure)
- **Failed Attempt Tracking**: Monitor and log failed authentication attempts

### 📊 Data Management
- **SQLite Database**: User credentials, logs, and failed attempts stored in a local SQLite database
- **Users Table**: Stores email, hashed password, and account creation date
- **Logs Table**: Records email, timestamp, and login result (Success/Fail)
- **Failed Attempts Table**: Tracks failed login attempts with timestamps for lockout enforcement
- **Messages Table**: Stores chat messages with timestamps

### 🎨 User Interface
- **Responsive Web Interface**: Clean, modern UI with dark theme
- **Real-time Feedback**: Instant validation messages for login and registration
- **Password Toggle**: Show/hide password visibility
- **Auto-generated Passwords**: One-click strong password generation for registration

## Technology Stack
- **Backend**: Flask (Python), Flask-SocketIO
- **Password Hashing**: bcrypt
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Security**: Regex-based validation, rate limiting

## Prerequisites
- Python 3.10+
- Dependencies: `pip install -r requirements.txt`

## Installation

1. Clone the repository
```bash
git clone https://github.com/willj768/Authentication-System.git
cd Authentication-System
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
```
Then open `.env` and fill in your values:
```
TEST_MODE=False
TEST_EMAIL=
TEST_PASSWORD=
FLASK_DEBUG=false
```

5. Run the Flask app
```bash
python src/app.py
```

6. Open in browser
```
http://127.0.0.1:5000        # local
http://<your-pi-ip>:5000     # from another device on the network
```

> ⚠️ Never commit your `.env` file. It is included in `.gitignore` by default.

## Project Structure

```
Authentication-System/
│
├── data/
│   └── auth.db                     # SQLite database (users, logs, failed_attempts, messages)
│
├── screenshots/
│   ├── errormsg.png
│   ├── login.png
│   └── pwgen.png
│
├── src/
│   ├── auth/
│   │   ├── __init__.py             # Exposes register, login, generateRandomPassword
│   │   ├── auth.py                 # Core register and login logic
│   │   ├── config.py               # Constants, file paths, and environment variables
│   │   ├── data_validation.py      # Email and password validation
│   │   ├── db_handler.py           # SQLite database connection and query functions
│   │   ├── logger.py               # Login attempt logging
│   │   ├── password_utils.py       # Random password generation
│   │   └── user_lockout.py         # Failed attempt tracking and account lockout
│   │
│   ├── chat/
│   │   ├── __init__.py             # Exposes chat functions
│   │   ├── chat.py                 # Chat room logic and message handling
│   │   └── db_handler.py           # Chat-specific database queries
│   │
│   └── app.py                      # Main Flask application and route handlers
│
├── static/
│   ├── chat.css                    # Chat room styling
│   ├── chat.js                     # Client-side WebSocket and chat logic
│   ├── script.js                   # Client-side JavaScript for auth forms
│   └── style.css                   # Dark theme styling for responsive web interface
│
├── templates/
│   ├── chat.html                   # Chat room HTML template
│   └── index.html                  # Main HTML template for Flask
│
├── .gitignore                      # Git ignore rules
├── README.md                       # Project documentation
└── requirements.txt                # Project dependencies
```

## License
MIT License - see [LICENSE](LICENSE) for details
