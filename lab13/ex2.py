from flask import Flask, render_template, request

app = Flask(__name__)

USERS = {
    "port": "port123",
    "ethan": "ethan123",
}

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if USERS.get(username) == password:
            return render_template("success.html", username=username)

        return render_template("login.html", error="Invalid username or password.")

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)