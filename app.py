from flask import Flask, render_template, request, redirect, url_for, session, flash, g
import sqlite3, os, json
from datetime import datetime

BASE = os.path.dirname(__file__)
DB = os.path.join(BASE, "app.db")
QUESTIONS_FILE = os.path.join(BASE, "questions.json")

app = Flask(__name__)
app.secret_key = "change-me-in-production"

def get_db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

@app.before_request
def load_user():
    g.user = None
    uid = session.get("uid")
    if uid:
        con = get_db()
        user = con.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
        g.user = user

@app.route("/", methods=["GET"])
def root():
    if session.get("uid"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email","").strip().lower()
        pw = request.form.get("password","")
        if not email or not pw:
            flash("Email and password required.")
            return render_template("register.html")
        con = get_db()
        try:
            con.execute("INSERT INTO users(email,password) VALUES(?,?)", (email, pw))
            con.commit()
        except sqlite3.IntegrityError:
            flash("Email already registered.")
            return render_template("register.html")
        user = con.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        session["uid"] = user["id"]
        flash("Account created. Welcome!")
        return redirect(url_for("dashboard"))
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email","").strip().lower()
        pw = request.form.get("password","")
        con = get_db()
        user = con.execute("SELECT * FROM users WHERE email=? AND password=?", (email, pw)).fetchone()
        if user:
            session["uid"] = user["id"]
            flash("Welcome back!")
            return redirect(url_for("dashboard"))
        flash("Invalid credentials.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Signed out.")
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if not session.get("uid"):
        return redirect(url_for("login"))
    con = get_db()
    attempts = con.execute("SELECT created_at, score FROM attempts WHERE user_id=? ORDER BY created_at DESC LIMIT 5", (session["uid"],)).fetchall()
    return render_template("dashboard.html", attempts=attempts)

def load_questions():
    with open(QUESTIONS_FILE, "r") as f:
        return json.load(f)

def score_answer(ans: str, keywords: list) -> int:
    # Simple keyword matching (case-insensitive). Each unique keyword matched = 1 point.
    text = ans.lower()
    seen = set()
    pts = 0
    for k in keywords:
        k_lower = k.lower()
        if k_lower in text and k_lower not in seen:
            seen.add(k_lower)
            pts += 1
    return pts

@app.route("/interview", methods=["GET","POST"])
def interview():
    if not session.get("uid"):
        return redirect(url_for("login"))
    questions = load_questions()
    if request.method == "POST":
        detailed = []
        total = 0
        max_per_q = 3 
        for q in questions:
            ans = request.form.get(f"answer_{q['id']}", "")
            pts = min(score_answer(ans, q["keywords"]), max_per_q)
            total += pts
            msg = "Good coverage." if pts >= 2 else "Too brief or missing key points."
            detailed.append(type("Obj",(object,),{"score": pts, "message": msg, "tip": q["tips"]}))
        max_score = max_per_q * len(questions)
        # Save attempt
        con = get_db()
        con.execute("INSERT INTO attempts(user_id, score) VALUES(?,?)", (session["uid"], total))
        con.commit()
        return render_template("result.html", total_score=total, max_score=max_score, detailed=detailed)
    return render_template("interview.html", questions=questions)

if __name__ == "__main__":
    app.run(debug=True)
