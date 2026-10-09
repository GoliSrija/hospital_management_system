import os
import sqlite3
from functools import wraps
from flask import Flask, jsonify, request, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
secret = os.environ.get("SECRET_KEY")
if not secret and os.environ.get("FLASK_ENV") == "production":
    raise RuntimeError("Set SECRET_KEY in the production environment.")
app.config.update(
    SECRET_KEY=secret or "LOCAL-ONLY-CHANGE-THIS-SECRET",
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE=os.environ.get("SESSION_COOKIE_SAMESITE", "Lax"),
    SESSION_COOKIE_SECURE=os.environ.get("SESSION_COOKIE_SECURE", "false").lower() == "true",
)
FRONTEND_ORIGIN = os.environ.get("FRONTEND_ORIGIN", "http://127.0.0.1:8000").rstrip("/")
DATABASE_PATH = os.environ.get("DATABASE_PATH", os.path.join(os.path.dirname(__file__), "app.db"))
CORS(app, resources={r"/api/*": {"origins": [FRONTEND_ORIGIN]}}, supports_credentials=True)

def connect_db():
    db = sqlite3.connect(DATABASE_PATH)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with connect_db() as db:
        db.execute(
            "CREATE TABLE IF NOT EXISTS users ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, "
            "email TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL, "
            "created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)"
        )

def require_login(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            return jsonify(message="Please sign in first."), 401
        return fn(*args, **kwargs)
    return wrapped

@app.get("/")
def home():
    return jsonify(status="running", service="generated-app-api")

@app.get("/health")
def health():
    return jsonify(status="healthy")

@app.post("/api/auth/register")
def register():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    password = data.get("password", "")
    if not username or len(username) > 120 or not email or len(email) > 254:
        return jsonify(message="Enter a valid name and email."), 400
    if not isinstance(password, str) or len(password) < 8 or len(password) > 1024:
        return jsonify(message="Password must be at least 8 characters."), 400
    try:
        with connect_db() as db:
            cur = db.execute("INSERT INTO users(username,email,password_hash) VALUES(?,?,?)",
                (username,email,generate_password_hash(password)))
            user_id = cur.lastrowid
    except sqlite3.IntegrityError:
        return jsonify(message="An account with this email already exists."), 409
    session.clear()
    session["user_id"] = user_id
    session["username"] = username
    return jsonify(message="Account created.", user={"id":user_id,"username":username,"email":email}), 201

@app.post("/api/auth/login")
def login():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    password = data.get("password", "")
    with connect_db() as db:
        user = db.execute("SELECT id,username,email,password_hash FROM users WHERE email=?",(email,)).fetchone()
    if not user or not isinstance(password,str) or not check_password_hash(user["password_hash"],password):
        return jsonify(message="Invalid email or password."), 401
    session.clear()
    session["user_id"] = user["id"]
    session["username"] = user["username"]
    return jsonify(message="Signed in.",user={"id":user["id"],"username":user["username"],"email":user["email"]})

@app.get("/api/auth/me")
@require_login
def me():
    with connect_db() as db:
        user = db.execute("SELECT id,username,email FROM users WHERE id=?",(session["user_id"],)).fetchone()
    if not user:
        session.clear()
        return jsonify(message="Please sign in again."), 401
    return jsonify(user=dict(user))

@app.post("/api/auth/logout")
def logout():
    session.clear()
    return jsonify(message="Signed out.")

@app.errorhandler(404)
def not_found(_error):
    return jsonify(message="Endpoint not found."), 404

@app.errorhandler(500)
def server_error(_error):
    app.logger.exception("Unhandled server error")
    return jsonify(message="Internal server error."), 500

init_db()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT","5001")), debug=False)
