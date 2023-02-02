DROP TABLE IF EXISTS notes;
DROP TABLE IF EXISTS tags;

CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tag INTEGER,
    title TEXT NOT NULL,
    body TEXT,
    date TEXT
);

CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_name TEXT NOT NULL,
    bg_color TEXT NOT NULL
);