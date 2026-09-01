PRAGMA user_version = 2;

-- create courses table and make initial course
CREATE TABLE IF NOT EXISTS courses
(
    course_id INTEGER PRIMARY KEY,
    course_name TEXT,
    course_sem VARCHAR(16),
    course_url VARCHAR(32)
);
INSERT INTO courses VALUES (0, 'Default Course', '-', 'default');

-- create enrollments table and enroll current users into this course
CREATE TABLE IF NOT EXISTS enrollments
(
    course_id INTEGER,
    user_id INTEGER,
    course_role STRING,
    last_swipe STRING
);
INSERT INTO enrollments (course_id, user_id, course_role, last_swipe)
SELECT 0, users.user_id, users.course_role, users.last_swipe
FROM users WHERE users.deleted = FALSE;

ALTER TABLE users DROP COLUMN last_swipe;

UPDATE enrollments SET course_role = 'instructor' WHERE course_role = 'admin';

-- add course to old tables
ALTER TABLE hardware ADD COLUMN course_id INTEGER DEFAULT 0;
ALTER TABLE queue ADD COLUMN course_id INTEGER DEFAULT 0;
ALTER TABLE visits ADD COLUMN course_id INTEGER DEFAULT 0;

-- turn admin course role into site-wide admin role
ALTER TABLE users RENAME course_role TO site_role;
UPDATE users SET site_role = 'user' WHERE site_role != 'admin';