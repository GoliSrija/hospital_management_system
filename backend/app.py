
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():

    return {
        "project": "hospital_management_system",
        "status": "running"
    }


@app.route("/api/login", methods=["POST"])
def login():

    return jsonify({
        "success": True,
        "message": "Login Successful"
    })


@app.route("/api/register", methods=["POST"])
def register():

    return jsonify({
        "success": True,
        "message": "Registration Successful"
    })


@app.route("/health")
def health():

    return {
        "status": "healthy"
    }


if __name__ == "__main__":
    app.run(debug=True)
