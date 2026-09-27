from flask import Flask, request, render_template

app = Flask(__name__)

users = {}

with open("users.txt") as f:
    for line in f:
        username, password_hash = line.strip().split(":")
        users[username] = password_hash

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        import hashlib
        password_hash = hashlib.md5(password.encode()).hexdigest()

        if username in users and users[username] == password_hash:
            if username == "admin":
                return "cebroid{breakfast_without_salt}"
            return "Login successful!"

        message = "Invalid username or password"

    return render_template("login.html", message=message)

app.run(host="0.0.0.0", port=5000)