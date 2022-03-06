from db import db
from flask import session

def new_message(creator_id, thread_id, content):
    sql = ("INSERT INTO messages (creator_id, thread_id, content, created_at, modified) VALUES (:creator_id, :thread_id, :content, NOW(), NOW())")
    db.session.execute(sql, {"creator_id":creator_id, "thread_id":thread_id, "content":content})
    db.session.commit()

def get_message(message_id):
    sql = ("SELECT U.id, M.content, M.thread_id, M.id FROM messages M, users U WHERE U.id=M.creator_id AND M.id=:message_id")
    result = db.session.execute(sql, {"message_id":message_id}).fetchone()
    return result

def get_messages(thread_id):
    sql = "SELECT U.id, U.username, M.id, M.content, M.created_at, M.modified, M.thread_id FROM users U, messages M WHERE U.id=M.creator_id AND M.thread_id=:thread_id ORDER BY M.created_at"
    results = db.session.execute(sql, {"thread_id":thread_id}).fetchall()
    return results

def modify_message(message_id, content, user_id):
    sql = ("SELECT U.id FROM users U, messages M WHERE M.creator_id=U.id AND M.id=:message_id")
    result = db.session.execute(sql, {"message_id":message_id}).fetchone()
    if result[0] != user_id:
        return False
    
    sql = ("UPDATE messages SET content=:content, modified=NOW() WHERE id=:message_id")
    db.session.execute(sql, {"content":content, "message_id":message_id})
    db.session.commit()
    return True

def delete_messages(thread_id):
    sql = ("DELETE FROM messages WHERE thread_id=:thread_id")
    db.session.execute(sql, {"thread_id":thread_id})
    db.session.commit()

def delete_message(message_id, user_id):
    sql = ("SELECT U.id FROM users U, messages M WHERE M.creator_id=U.id AND M.id=:message_id")
    result = db.session.execute(sql, {"message_id":message_id}).fetchone()
    if result[0] != user_id:
        return False
    
    sql = ("DELETE FROM messages WHERE id=:message_id")
    db.session.execute(sql, {"message_id":message_id})
    db.session.commit()
    return True