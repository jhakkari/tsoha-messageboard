from app import app
from flask import render_template, request, redirect, session
import users, topics, threads, messages, followed


@app.route("/")
def index():
    if users.user_id() == 0:
        return render_template("index.html")
    elif session["user_group"] != 0:
        general_topics = topics.get_general_topics()
        hidden_topics = topics.get_hidden_topics(session["user_group"])
        return render_template("index.html", general_topics=general_topics, hidden_topics=hidden_topics)
    else:
        general_topics = topics.get_general_topics()
        return render_template("index.html", general_topics=general_topics)

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
        role = request.form["user_group"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1, role):
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
        return redirect("/admin")
    else:
        render_template("error.html", message="Ei vaadittavia oikeuksia.")

@app.route("/topics/delete", methods=["POST"])
def delete_topic():
    if users.user_id() == 0:
        return render_template("error.html", message="Kirjaudu sisään jatkaaksesi.")
    elif users.is_admin():
        topics.delete_topic(request.form["topic_id"])
        return redirect("/admin")
    else:
        return render_template("error.html", message="Ei vaadittavia oikeuksia.")


@app.route("/threads/<int:id>", methods=["GET", "POST"])
def theads(id):
    if users.user_id() == 0:
        return redirect("/")
    elif session["user_group"] != 0:
        general_threads = threads.get_general_threads(id)
        hidden_threads = threads.get_hidden_threads(id, session["user_group"])
        return render_template("threads.html", general_threads=general_threads, hidden_threads=hidden_threads)
    else:
        general_threads = threads.get_general_threads(id)
        return render_template("threads.html", general_threads=general_threads)

@app.route("/threads/new", methods=["POST"])
def new_thread():
    if users.user_id() == 0:
        return render_template("error.html", message="Kirjaudu sisään jatkaaksesi.")
    topic_id = request.form["topic_id"]
    if topics.check_access(topic_id, session["user_group"]):
        creator_id = users.user_id()
        subject = request.form["subject"]
        content= request.form["content"]
        visibility = request.form["visibility"]
        threads.new_thread(topic_id, creator_id, subject, content, visibility)
        return redirect("/threads/" + str(topic_id))
    return render_template("error.html", message="Ei vaadittavia oikeuksia.")

@app.route("/thread/<int:id>")
def thread(id):
    if users.user_id() == 0:
        return render_template("error.html", "Kirjaudu sisään jatkaaksesi.")
    elif threads.check_access(id, session["user_group"]):
        contents = threads.get_thread(id)
        reply_messages = messages.get_messages(id)
        return render_template("thread.html", subject=contents[0], content=contents[1], username=contents[4], created_at=contents[2], user_id=contents[6], reply_messages=reply_messages, thread_id=id)
    else:
        return render_template("error.html", message="Ei vaadittavia oikeuksia.")

@app.route("/thread/modify", methods=["POST"])
def modify_thread():
    if users.user_id() == 0:
        return render_template("error.html", message="Kirjaudu sisään jatkaaksesi.")
    thread = threads.get_thread(request.form["thread_id"])
    if thread[6] == session["user_id"]:
        return render_template("modifythread.html", thread_id=thread[7], subject=thread[0], content=thread[1])
    else:
        render_template("error.html", message="Ei vaadittavia oikeuksia.")

@app.route("/thread/modify/save", methods=["POST"])
def save_modified_thread():
    if users.user_id() == 0:
        render_template("error.html", messages="kirjaudu sisään jatkaaksesi.")
    thread_id = request.form["thread_id"]
    if threads.modify_thread(thread_id, request.form["modified_subject"], request.form["modified_content"], users.user_id()):
        return redirect("/thread/" + str(thread_id))
    else:
        return render_template("error.html", message="Ei vaadittavia oikeuksia.")

@app.route("/messages/new", methods=["POST"])
def new_message():
    if users.user_id() == 0:
        return render_template("error.html", message="Kirjaudu sisään jatkaaksesi.")
    thread_id = request.form["thread_id"]
    if threads.check_access(thread_id, session["user_group"]):
        creator_id = users.user_id()
        content = request.form["message_content"]
        messages.new_message(creator_id, thread_id, content)
        return redirect("/thread/" + str(thread_id))
    else:
        return render_template("error.html", message="Et voi vastata tähän viestiketjuun.")

@app.route("/messages/modify", methods=["POST"])
def modify_message():
    if users.user_id() == 0:
        return render_template("error.html", message="Kirjaudu sisään jatkaaksesi.")
    message = messages.get_message(request.form["message_id"])
    if message[0] == session["user_id"]:
        return render_template("modifymessage.html", message_id=message[0], content=message[1])
    else:
        return render_template("error.html", message="Ei vaadittavia oikeuksia.")

@app.route("/messages/modify/save", methods=["POST"])
def save_modified_message():
    if users.user_id() == 0:
        render_template("error.html", message="Kirjaudu sisään jatkaaksesi.")
    message_id = request.form["message_id"]
    if messages.modify_message(message_id, request.form["modified_content"], session["user_id"]):
        message = messages.get_message(message_id)
        return redirect("/thread/" + str(message[2]))
    else:
        return render_template("error.html", message="Ei vaadittavia oikeuksia.")
    


@app.route("/followed")
def followed_threads():
    if users.user_id() == 0:
        return render_template("error.html", message="Kirjaudu sisään jatkaaksesi.")
    threads = followed.get_followed_threads(users.user_id())
    return render_template("followed.html", followed_threads=threads)

@app.route("/followed/add", methods=["POST"])
def add_followed():
    if users.user_id() == 0:
        return render_template("error.html", message="Kirjaudu sisään jatkaaksesi.")
    thread_id = request.form["thread_id"]
    followed.add_followed_threads(users.user_id(), thread_id)
    return redirect("/thread/" + str(thread_id))

@app.route("/admin")
def admin():
    if users.user_id() == 0:
        return render_template("error.html", message="Kirjaudu sisän jatkaaksesi.")
    elif users.is_admin():
        general_topics = topics.get_general_topics()
        hidden_topics = topics.get_hidden_topics(1)
        return render_template("admin.html", general_topics=general_topics, hidden_topics=hidden_topics)
    else:
        return render_template("error.html", message="Ei vaadittavia oikeuksia.")