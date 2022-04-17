DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS deadline;

DROP TABLE IF EXISTS verification;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username VARCHAR(30) UNIQUE NOT NULL,
  password VARCHAR(30) NOT NULL,
  photoLink VARCHAR(100)
);

CREATE TABLE verification (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username VARCHAR(30) NOT NULL,
  ver_code INTEGER
);

CREATE TABLE deadline (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(30) NOT NULL,
  time DATETIME NOT NULL,
  from_bb BIT,
  set_reminder BIT,
  user_id INTEGER,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

INSERT INTO user (username,password) VALUES ('admin', 'admin');

select id, username, password from user where username = 'admin';

COMMIT;

select id, username, password from user;