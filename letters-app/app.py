from flask import Flask, render_template, request, redirect, url_for
import datetime

app = Flask(__name__)

PASSWORD = "secret123"

@app.route('/')
def home():
    return "Welcome! Try /letter/1"

@app.route('/letter/<letter_id>', methods=['GET', 'POST'])
def letter(letter_id):
    if request.method == 'POST':
        password = request.form.get('password')
        if password == PASSWORD:
            # Log access
            with open("access_log.txt", "a") as log:
                log.write(f"{datetime.datetime.now()} - Letter {letter_id} accessed\n")
            return redirect(url_for('view_letter', letter_id=letter_id))
        else:
            return render_template("login.html", error="Wrong password.")
    return render_template("login.html")

@app.route('/letter/<letter_id>/view')
def view_letter(letter_id):
    try:
        with open(f"letters/{letter_id}.html", "r") as f:
            content = f.read()
        return render_template("letter.html", content=content)
    except FileNotFoundError:
        return "Letter not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
