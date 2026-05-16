from flask import Flask, request, jsonify, render_template, session, redirect
from auth import register, login, generateRandomPassword
import os
from auth.db_handler import initDB
from flask_socketio import SocketIO, emit
#from chat import sendMessage, loadHistory

initDB()

projectRoot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

templateDir = os.path.join(projectRoot, "templates")
staticDir = os.path.join(projectRoot, "static")

app = Flask(__name__, template_folder=templateDir, static_folder=staticDir)
app.config["SECRET_KEY"] = "your-secret-key"
socketio = SocketIO(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def registerRoute():
    data = request.json
    success, message = register(data["email"], data["password"], data["confirmPassword"])
    return jsonify({"success": success, "message": message})

@app.route("/login", methods=["POST"])
def loginRoute():
    data = request.json
    success, message = login(data["email"], data["password"])
    return jsonify({"success": success, "message": message})

@app.route("/generate-password", methods=["GET"])
def generatePasswordRoute():
    return jsonify({"password": generateRandomPassword()})

@app.route("/chat")
def chatRoute():
    if "email" not in session:
        return redirect("/")
    return render_template("chat.html")

@socketio.on("connect")
def handleConnect():
    history = loadHistory()
    emit("history", history)

def handleMessage(data):
    email = session.get("email", "unknown")
    sendMessage(email, data["message"])
    emit("message", {"email": email, "message": data["message"]}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")




