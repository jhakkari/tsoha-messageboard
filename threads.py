from db import db
from flask import session

def new_thread(topic_id, creator_id, subject, content, visibility):
    sql = ("INSERT INTO topics (topic_id, creator_id, created_at, subject, content, visibility, modified) VALUES (:topic_id, :creator_id, NOW(), :subject, :content, :visibility, NOW())")
    db.session.execute(sql, {"topic_id":topic_id, "creator_id":creator_id, "subject":subject, "content":content, "visibility":visibility})
    db.session.commit

def get_thread(id):
    sql = ("SELECT T.subject, T.content, T.created_at, T.modified, U.username, U.role FROM threads T, users U WHERE T.creator_id=U.id AND T.id=:id")
    result = db.session.execute(sql, {"id":id}).fetchone()
    return result

def get_general_threads(topic_id):
    sql = ("SELECT T.id, T.subject, T.created_at, U.username FROM threads T, users U WHERE T.creator_id=U.id AND topic_id=:topic_id AND T.visibility=0")
    results = db.session.execute(sql, {"topic_id":topic_id}).fetchall()
    return results

def get_hidden_threads(topic_id, visibility):
    if visibility == 1:
        sql = ("SELECT T.id, T.subject, T.created_at, U.username FROM threads T, users U WHERE T.creator_id=U.id AND topic_id=:topic_id AND T.visibility >0")
        results = db.session.execute(sql, {"topic_id":topic_id}).fetchall()
        return results
    else:
        sql = ("SELECT T.id, T.subject, T.created_at, U.username FROM threads T, users U WHERE T.creator_id=U.id AND topic_id=:topic_id AND T.visibility=:visibility")
        results = db.session.execute(sql, {"topic_id":topic_id, "visibility":visibility}).fetchall()
        return results

def check_access(thread_id, user_group):
    sql = ("SELECT visibility FROM threads WHERE id=:thread_id")
    results = db.session.execute(sql, {"thread_id":thread_id}).fetchone()
    if results[0] == 0 and user_group > 1:
        return True
    elif results[0] == user_group:
        return True
    elif user_group == 1:
        return True
    else:
        return False