from flask import Flask, request, jsonify, render_template
from auth import register, login, generateRandomPassword
import os

projectRoot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

templateDir = os.path.join(projectRoot, "templates")
staticDir = os.path.join(projectRoot, "static")

app = Flask(__name__, template_folder=templateDir, static_folder=staticDir)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def registerRoute():
    data = request.json
    success, message = register(data["email"], data["password"], data["confirmPassword"])

    if data["password"] != data["confirmPassword"]:
        return jsonify({"success": False, "message": "Passwords do not match"})
    return jsonify({"success": success, "message": message})

@app.route("/login", methods=["POST"])
def login_route():
    data = request.json
    success, message = login(data["email"], data["password"])
    return jsonify({"success": success, "message": message})

@app.route("/generate-password", methods=["GET"])
def generatePasswordRoute():
    password = generateRandomPassword()
    confirmPassword = password
    return jsonify({"password": password, "confirmPassword": confirmPassword})

if __name__ == "__main__":
    app.run(debug=True)

