## Project Structure

```
Authentication-System/
├── app/
│   ├── app.py              – Main Flask application and route handlers
│   └── auth.py             – Authentication logic, password hashing, and validation utilities
├── data/
│   ├── userdata.csv        – Stores user emails, hashed passwords, and creation dates
│   ├── logs.csv            – Records all login attempts (email, timestamp, success/failure)
│   └── failedattempts.csv  – Tracks failed login attempts for account lockout enforcement
├── static/
│   ├── style.css           – Dark theme styling for responsive web interface
│   └── script.js           – Client-side JavaScript for form handling and API calls
├── templates/
│   └── index.html          – Main HTML template for Flask
├── README.md               – Project documentation
└── .gitignore              – Git ignore rules
```