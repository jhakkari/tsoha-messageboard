from db import db
from flask import session
import users, threads

def new_topic(creator_id, subject, visibility):
    sql = ("INSERT INTO topics (creator_id, subject, visibility) VALUES (:creator_id, :subject, :visibility)")
    db.session.execute(sql, {"creator_id":creator_id, "subject":subject, "visibility":visibility})
    db.session.commit()

def get_general_topics():
    sql = "SELECT id, subject FROM topics WHERE visibility=0"
    results = db.session.execute(sql)
    return results

def get_hidden_topics(visibility):
    if visibility == 1:
        sql = ("SELECT id, subject FROM topics WHERE visibility BETWEEN 1 AND 4")
        results = db.session.execute(sql).fetchall()
        return results
    else:
        sql = ("SELECT id, subject FROM topics WHERE visibility=:visibility")
        results = db.session.execute(sql, {"visibility":visibility}).fetchall()
        return results

def check_access(topic_id, user_group):
    sql = ("SELECT visibility FROM topics WHERE id=:topic_id")
    results = db.session.execute(sql, {"topic_id":topic_id}).fetchone()
    if results[0] == 0 and user_group > 1:
        return True
    elif results[0] == user_group:
        return True
    elif user_group == 1:
        return True
    else:
        return False

def delete_topic(topic_id):
    sql = ("SELECT id FROM threads WHERE topic_id=:topic_id")
    results = db.session.execute(sql, {"topic_id":topic_id}).fetchall()
    for id in results:
        threads.delete_thread(id[0])
    sql = ("DELETE FROM topics WHERE id=:topic_id")
    db.session.execute(sql, {"topic_id":topic_id})
    db.session.commit()
