from flask import Flask, render_template, request, redirect, url_for
import os
import datetime

# Ensure Flask knows exactly where templates are
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)

app.secret_key = "supersecretkey"  # change this to something unique!

# dictionary of letter_id → password
LETTER_PASSWORDS = {
    "1": "sunshine",
    "2": "birthday",
    "3": "secret"
}

@app.route("/", methods=["GET"])
def home():
    return "<h2>Welcome to Letters for My Son</h2><p>Visit /letter/1, /letter/2, etc.</p>"

@app.route("/letter/<letter_id>", methods=["GET", "POST"])
def login(letter_id):
    if letter_id not in LETTER_PASSWORDS:
        return "Letter not found", 404

    if request.method == "POST":
        entered = request.form.get("password")
        if entered == LETTER_PASSWORDS[letter_id]:
            session[f"authenticated_{letter_id}"] = True
            # log the access
            with open("access_log.txt", "a") as f:
                f.write(f"Letter {letter_id} accessed at {datetime.now()} from {request.remote_addr}\n")
            return redirect(url_for("letter", letter_id=letter_id))
        else:
            return render_template("login.html", error="Incorrect password", letter_id=letter_id)

    return render_template("login.html", letter_id=letter_id)

@app.route("/letter/<letter_id>/view")
def letter(letter_id):
    if not session.get(f"authenticated_{letter_id}"):
        return redirect(url_for("login", letter_id=letter_id))

    letter_file = os.path.join("letters", f"{letter_id}.html")
    if not os.path.exists(letter_file):
        return "Letter file not found", 404

    with open(letter_file, "r") as f:
        content = f.read()
    return render_template("letter.html", content=content)

@app.route("/log")
def view_log():
    if not os.path.exists("access_log.txt"):
        return "No log entries yet."
    with open("access_log.txt", "r") as f:
        logs = f.readlines()
    return "<br>".join(logs)