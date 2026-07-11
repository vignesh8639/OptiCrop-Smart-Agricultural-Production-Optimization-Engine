import pickle
import sqlite3
import numpy as np

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from utils.predictor import CropPredictor

app = Flask(__name__)
app.secret_key = "smart_agriculture_secret_key"

# -----------------------------
# Database
# -----------------------------
DATABASE = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------------
# ML Model
# -----------------------------
model = pickle.load(open("crop_model.pkl", "rb"))
predictor = CropPredictor()

# -----------------------------
# Home (redirect to login)
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")

# -----------------------------
# Register
# -----------------------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        ).fetchone()

        if user:
            flash("Email already registered!", "danger")
            conn.close()
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        conn.execute(
            "INSERT INTO users(fullname, email, password) VALUES (?, ?, ?)",
            (fullname, email, hashed_password)
        )

        conn.commit()
        conn.close()

        flash("Registration Successful! Please Login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# -----------------------------
# Login
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):

            session["user_id"] = user["id"]
            session["fullname"] = user["fullname"]

            flash("Login Successful!", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid Email or Password", "danger")

    return render_template("login.html")

# -----------------------------
# Dashboard
# -----------------------------
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        name=session["fullname"]
    )

# -----------------------------
# Prediction
# -----------------------------
@app.route("/predict", methods=["POST"])
def predict_route():

    if "user_id" not in session:
        return redirect(url_for("login"))

    try:
        data = request.form

        # Convert form inputs into numeric array
        features = [float(data[key]) for key in data.keys()]
        final_features = np.array([features])

        # Use your ML model directly
        prediction = model.predict(final_features)[0]

        return render_template(
            "dashboard.html",
            name=session["fullname"],
            prediction=prediction
        )

    except Exception as e:
        flash(f"Prediction Error: {str(e)}", "danger")
        return redirect(url_for("dashboard"))

# -----------------------------
# Logout
# -----------------------------
@app.route("/logout")
def logout():

    session.clear()
    flash("Logged Out Successfully!", "success")
    return redirect(url_for("login"))

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)