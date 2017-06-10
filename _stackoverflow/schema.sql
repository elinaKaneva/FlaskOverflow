drop table if exists questions;
drop table if exists answers;

create table questions (
  id integer primary key autoincrement,
  title text not null,
  'text' text not null
);

create table answers (
  id integer primary key autoincrement,
  'text' text not null,
  qid integer references questions(id)
);
