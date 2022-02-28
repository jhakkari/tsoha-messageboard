from db import db
from flask import session

def add_followed_threads(user_id, thread_id):
    sql = ("INSERT INTO followed (user_id, thread_id, added_at) VALUES (:user_id, :thread_id, NOW()))")
    db.session.execute(sql, {"user_id":user_id, "thread_id":thread_id})
    db.session.commit()


def get_followed_threads(user_id):
    sql = ("SELECT T.subject, F.thread_id, F.added_at FROM followed F, threads T WHERE F.user_id=:user_id AND F.thread_id=T.id")
    results = db.session.execute(sql, {"user_id":user_id}).fetchall()
    return results

def remove_followed_thread(user_id, thread_id):
    sql = ("DELETE FROM followed WHERE user_id=:user_id AND thread_id=:thread_id")
    db.session.execute(sql, {"user_id":user_id, "thread_id":thread_id})
    db.session.commit()