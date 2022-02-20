CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role INTEGER
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users,
    subject TEXT,
    visibility INTEGER
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES topics,
    creator_id INTEGER REFERENCES users,
    created_at TIMESTAMP
    subject TEXT,
    content TEXT,
    visibility INTEGER,
    modified TIMESTAMP
);