import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from urllib.parse import urlparse

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///tasks.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate form
        if not name or not username or not password or not confirmation:
            flash("Please fill out all fields.")
            return render_template("register.html")

        if password != confirmation:
            flash("Passwords do not match.")
            return render_template("register.html")

        if password != confirmation:
            flash("Passwords do not match.")
            return render_template("register.html")

        if len(password) < 8:
            flash("Password must be at least 8 characters long.")
            return render_template("register.html")

        # Check if username already exists
        existing = db.execute("SELECT * FROM users WHERE username = ?", username)
        if existing:
            flash("Username already exists.")
            return render_template("register.html")

        # Insert new user into database with hashed password
        hashed_password = generate_password_hash(password)
        db.execute(
            "INSERT INTO users (name, username, password) VALUES (?, ?, ?)",
            name, username, hashed_password
        )

        flash("Registered successfully! You can now log in.")
        return redirect("/")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Validate submission
        if not username or not password:
            flash("Must provide both username and password.")
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password matches hash
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], password):
            flash("Invalid username or password.")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        flash(f"Welcome back, {rows[0]['name']}!")
        return redirect("/home")

    return render_template("login.html")


@app.route("/home")
def home():
    if "user_id" not in session:
        return redirect("/")

    tasks = db.execute(
        "SELECT * FROM tasks WHERE user_id = ? AND is_complete = 0 ORDER BY due_date ASC",
        session["user_id"]
    )

    completed_count = db.execute(
        "SELECT COUNT(*) AS count FROM tasks WHERE user_id = ? AND is_complete = 1",
        session["user_id"]
    )[0]["count"]

    total_count = db.execute(
        "SELECT COUNT(*) AS count FROM tasks WHERE user_id = ?",
        session["user_id"]
    )[0]["count"]

    return render_template("home.html", tasks=tasks, completed_count=completed_count, total_count=total_count)


@app.route("/create", methods=["GET", "POST"])
def create():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        due_date = request.form.get("due_date")

        # Validation
        if not title:
            flash("Task title is required.")
            return render_template("create.html")

        db.execute(
            "INSERT INTO tasks (user_id, title, description, due_date) VALUES (?, ?, ?, ?)",
            session["user_id"], title, description, due_date or None
        )

        flash("Task created successfully!")
        return redirect("/home")

    return render_template("create.html")


@app.route("/complete/<int:task_id>", methods=["POST"])
def complete(task_id):
    if "user_id" not in session:
        return redirect("/login")

    # Update task if it belongs to the current user
    db.execute(
        "UPDATE tasks SET is_complete = 1 WHERE id = ? AND user_id = ?",
        task_id, session["user_id"]
    )

    flash("Task marked as complete!")
    return redirect("/home")


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    if "user_id" not in session:
        return redirect("/login")

    # Ensure the task belongs to the user before deleting
    db.execute(
        "DELETE FROM tasks WHERE id = ? AND user_id = ?",
        task_id, session["user_id"]
    )

    flash("Task deleted successfully.")

    # Redirect back to the page the request came from
    return redirect(request.referrer or "/home")


@app.route("/tasks")
def view_tasks():
    if "user_id" not in session:
        return redirect("/login")

    incomplete_tasks = db.execute(
        "SELECT * FROM tasks WHERE user_id = ? AND is_complete = 0 ORDER BY due_date DESC",
        session["user_id"]
    )

    completed_tasks = db.execute(
        "SELECT * FROM tasks WHERE user_id = ? AND is_complete = 1 ORDER BY due_date DESC",
        session["user_id"]
    )

    completed_count = db.execute(
        "SELECT COUNT(*) AS count FROM tasks WHERE user_id = ? AND is_complete = 1",
        session["user_id"]
    )[0]["count"]

    total_count = db.execute(
        "SELECT COUNT(*) AS count FROM tasks WHERE user_id = ?",
        session["user_id"]
    )[0]["count"]

    return render_template("tasks.html", incomplete_tasks=incomplete_tasks, completed_tasks=completed_tasks, completed_count=completed_count, total_count=total_count)



@app.route("/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    if "user_id" not in session:
        return redirect("/login")

    db.execute(
        "UPDATE tasks SET is_complete = 1 WHERE id = ? AND user_id = ?",
        task_id, session["user_id"]
    )

    flash("Task marked as complete.")

    # Get the redirect target from the form, fallback to /home
    next_page = request.form.get("next") or "/home"
    return redirect(next_page)


@app.route("/logout")
def logout():
    session.clear()
    flash("You’ve been logged out.")
    return redirect("/")
