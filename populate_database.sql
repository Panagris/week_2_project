-- CREATE TABLE users ( 
--     id INT(8) UNSIGNED NOT NULL auto_increment,
--     name VARCHAR(255) default NULL,
--     previous_subjects VARCHAR(255) default NULL,
--     PRIMARY KEY (id)
-- ) AUTO_INCREMENT=1;

CREATE TABLE subjects ( 
    subject_name VARCHAR(255) default NULL
);

INSERT INTO subjects (subject_name)
VALUES ("Math"), ("Physics"), ("English"), ("History"), 
("Computer Science");

CREATE TABLE study_methods ( 
    method_name TEXT(255) default NULL
);

INSERT INTO study_methods (method_name)
VALUES ("Question and Answer"), ("Explanation"), ("Quiz"), ("Flashcards");

CREATE TABLE subtopics ( 
    subject_name TEXT(255) default NULL,
    subtopic TEXT(255) default NULL,    
);

INSERT INTO study_methods (subject_name, subtopic)
VALUES ("Math", "Algebra"), ("English", "Literature"), 
("Physics", "Kinematics"), ("History", "American Revolution");