from db import db
from flask import session
import messages, followed

def new_thread(topic_id, creator_id, subject, content, visibility):
    sql = ("INSERT INTO topics (topic_id, creator_id, created_at, subject, content, visibility, modified) VALUES (:topic_id, :creator_id, NOW(), :subject, :content, :visibility, NOW())")
    db.session.execute(sql, {"topic_id":topic_id, "creator_id":creator_id, "subject":subject, "content":content, "visibility":visibility})
    db.session.commit

def get_thread(id):
    sql = ("SELECT T.subject, T.content, T.created_at, T.modified, U.username, U.role, U.id, T.id, T.topic_id FROM threads T, users U WHERE T.creator_id=U.id AND T.id=:id")
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

def modify_thread(thread_id, subject, content, user_id):
    sql = ("SELECT U.id FROM users U, threads T WHERE T.creator_id=U.id AND T.id=:thread_id")
    result = db.session.execute(sql, {"thread_id":thread_id}).fetchone()
    if result[0] != user_id:
        return False
    
    sql = ("UPDATE threads SET subject=:subject, content=:content, modified=NOW() WHERE id=:thread_id")
    db.session.execute(sql, {"subject":subject, "content":content, "thread_id":thread_id})
    db.session.commit()
    return True

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

def check_creator(thread_id, user_id):
    sql = ("SELECT U.id FROM threads T, users U WHERE T.creator_id=U.id AND T.id=:thread_id")
    results = db.session.execute(sql, {"thread_id":thread_id}).fetchone()
    if results[0] == user_id:
        return True
    else:
        return False

def delete_thread(thread_id):
    messages.delete_messages(thread_id)
    followed.delete_followings(thread_id)
    sql = ("DELETE FROM threads WHERE id=:thread_id")
    db.session.execute(sql, {"thread_id":thread_id})
    db.session.commit()
