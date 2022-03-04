from db import db
from flask import session

def new_message(creator_id, thread_id, content):
    sql = ("INSERT INTO messages (creator_id, thread_id, content, created_at, modified) VALUES (:creator_id, :thread_id, :content, NOW(), NOW())")
    db.session.execute(sql, {"creator_id":creator_id, "thread_id":thread_id, "content":content})
    db.session.commit()

def get_messages(thread_id):
    sql = "SELECT U.username, M.content, M.created_at, M.modified FROM users U, messages M WHERE U.id=M.creator_id AND M.thread_id=:thread_id ORDER BY M.created_at"
    results = db.session.execute(sql, {"thread_id":thread_id}).fetchall()
    return results

def delete_messages(thread_id):
    sql = ("DELETE FROM messages WHERE thread_id=:thread_id")
    db.session.execute(sql, {"thread_id":thread_id})
    db.session.commit()
