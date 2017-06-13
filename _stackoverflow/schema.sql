DROP TABLE if exists Question;
DROP TABLE if exists Answer;
DROP TABLE if exists Tag;
DROP TABLE if exists QuestionTag;

PRAGMA foreign_keys = "1";

CREATE TABLE Question (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  'text' TEXT NOT NULL
);

CREATE TABLE Answer (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  'text' TEXT NOT NULL,
  question_id INTEGER,
  FOREIGN KEY(question_id) REFERENCES Question(id)
);

CREATE TABLE Tag (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  CONSTRAINT 'name_unique' UNIQUE (name)
);

CREATE TABLE QuestionTag (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  question_id INTEGER,
  tag_id INTEGER,
  FOREIGN KEY(question_id) REFERENCES Question(id),
  FOREIGN KEY(tag_id) REFERENCES Tag(id)
);
