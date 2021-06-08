
DROP TABLE IF EXISTS posts;

CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);


CREATE TABLE users (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  lastname TEXT not null ,
  username text unique not null ,
  email TEXT UNIQUE NOT NULL,
  profile_pic TEXT NOT NULL
);

CREATE TABLE roles (
    id TEXT PRIMARY KEY ,
    name TEXT UNIQUE not null
)


