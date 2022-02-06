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