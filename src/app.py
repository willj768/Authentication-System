from flask import Flask, request, jsonify, render_template, session, redirect
from auth.auth import register, login
from auth.password_utils import generateRandomPassword
import os
from db_handler import initDB, sendMessage, getRecentMessages
from flask_socketio import SocketIO, emit
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import ALLOWED_ORIGINS, SECRET_KEY

initDB()

projectRoot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

templateDir = os.path.join(projectRoot, "templates")
staticDir = os.path.join(projectRoot, "static")

app = Flask(__name__, template_folder=templateDir, static_folder=staticDir)
app.config["SECRET_KEY"] = SECRET_KEY

app.config["SESSION_COOKIE_SAMESITE"] = "Strict"
app.config["SESSION_COOKIE_HTTPONLY"] = True

socketio = SocketIO(app, manage_session=False, cors_allowed_origins=ALLOWED_ORIGINS)

limiter = Limiter(get_remote_address, app=app)

#When the user visits the root URL, index.html is rendered
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["POST"]) #Listens for requests to register an account
@limiter.limit("5 per minute")
def registerRoute():
    data = request.get_json(silent=True) or {} #Extracts the email, password, and confirmPassword from the JSON body
    email = data.get("email", "")
    password = data.get("password", "")
    confirmPassword = data.get("confirmPassword", "")
    if not email or not password or not confirmPassword:
        return jsonify({"success": False, "message": "Missing Fields"}), 400
    success, message = register(email, password, confirmPassword) #Passes inputs to register function
    return jsonify({"success": success, "message": message})

@app.route("/login", methods=["POST"]) #Listens for requests to login
@limiter.limit("10 per minute")
def loginRoute():
    data = request.get_json(silent=True) or {} #Extracts the email and password from the JSON body
    email = data.get("email", "")
    password = data.get("password", "")
    if not email or not password:
        return jsonify({"success": False, "message": "Missing Fields"}), 400
    success, message = login(email, password) #Passes inputs to login function
    if success:
        session["email"] = data["email"] #Stores the user's email in the session upon a successful login
    return jsonify({"success": success, "message": message})

@app.route("/generate-password", methods=["GET"]) #Listens for GET requests to generate a password
def generatePasswordRoute():
    return jsonify({"password": generateRandomPassword()}) #Calls generateRandomPassword and returns result as JSON

@app.route("/chat")
def chatRoute():
    if "email" not in session:
        return redirect("/")
    return render_template("chat.html")

@socketio.on("connect")
def handleConnect():
    if "email" not in session:
        return False
    history = getRecentMessages()
    emit("history", history)

@socketio.on("message")
def handleMessage(data):
    if "email" not in session:
        return
    email = session.get("email")
    message = data.get("message", "").strip()
    if not message:
        return
    if len(message) > 500:
        return
    sendMessage(email, message)
    emit("message", {"email": email, "message": message}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True, debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")




