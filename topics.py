from db import db
from flask import session
import users

def new_topic(creator_id, subject, visibility):
    sql = ("INSERT INTO topics (creator_id, subject, visibility) VALUES (:creator_id :subject, :visibility)")
    db.session.execute(sql, {"creator_id":creator_id, "subject":subject, "visibility":visibility})
    db.session.commit()

def get_topics():
    sql = "SELECT id, subject FROM topics"
    results = db.session.execute(sql)
    return results
