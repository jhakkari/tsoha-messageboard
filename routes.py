from app import app
from flask import render_template, request, redirect
import users, topics


@app.route("/")
def index():
    if users.user_id() == 0:
        return render_template("index.html")
    else:
        all_topics = topics.get_topics()
        return render_template("index.html", topics=all_topics)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/topics/new", methods=["POST"])
def new_topic():
    if users.is_admin():
        creator_id = users.user_id()
        subject = request.form["subject"]
        visibility = request.form["visibility"]
        topics.new_topic(creator_id, subject, visibility)
        return redirect("/")
    else:
        render_template("error.html", message="Sinulla ei ole vaadittavia oikeuksia.")

