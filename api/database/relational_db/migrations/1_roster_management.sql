PRAGMA user_version = 1;

-- Making ubit and person_num unique means that a user cannot be re-enrolled if their original
-- account is deleted under normal circumstances. Unfortunately it is not possible to remove
-- this constraint. Thus, we're recreating the entire table here and taking the opportunity to
-- add the deleted column while we're at it.
CREATE TABLE users_new
(
    user_id         INTEGER PRIMARY KEY,
    preferred_name  VARCHAR(255),
    last_name       VARCHAR(255),
    ubit            VARCHAR(16),
    person_num      INTEGER,
    course_role     VARCHAR(16),
    last_swipe      TEXT
);

INSERT INTO users_new (user_id, preferred_name, last_name, ubit, person_num, course_role, last_swipe)
SELECT user_id, preferred_name, last_name, ubit, person_num, course_role, last_swipe FROM users;

ALTER TABLE users_new ADD COLUMN deleted DEFAULT false;
DROP TABLE users;
ALTER TABLE users_new RENAME TO users;