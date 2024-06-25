-- CREATE TABLE users ( 
--     id INT(8) UNSIGNED NOT NULL auto_increment,
--     name VARCHAR(255) default NULL,
--     previous_subjects VARCHAR(255) default NULL,
--     PRIMARY KEY (id)
-- ) AUTO_INCREMENT=1;

CREATE TABLE subjects ( 
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(255) default NULL
);

INSERT INTO subjects (subject_id, subject_name)
VALUES (1, "Math"), (2, "Physics"), (3, "English");