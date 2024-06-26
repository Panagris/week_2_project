CREATE TABLE IF NOT EXISTS users ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) default NULL
);

CREATE TABLE IF NOT EXISTS user_subjects ( 
    user_id INTEGER,
    subject_name VARCHAR(255),
    PRIMARY KEY (user_id, subject_name),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (subject_name) REFERENCES subjects(subject_name)
);

CREATE TABLE IF NOT EXISTS subjects ( 
    subject_name VARCHAR(255) default NULL,
    PRIMARY KEY (subject_name)
);

INSERT OR IGNORE INTO subjects (subject_name)
VALUES ("Math"), ("Physics"), ("English"), ("History"), 
("Computer Science");

CREATE TABLE IF NOT EXISTS study_methods ( 
    method_name TEXT(255) default NULL,
    PRIMARY KEY (method_name)
);

INSERT OR IGNORE INTO study_methods (method_name)
VALUES ("Question and Answer"), ("Explanation"), ("Quiz"), ("Flashcards");

CREATE TABLE IF NOT EXISTS subtopics ( 
    subject_name TEXT(255) default NULL,
    subtopic TEXT(255) default NULL,
    PRIMARY KEY (subtopic)
);

INSERT OR IGNORE INTO subtopics (subject_name, subtopic)
VALUES ("Math", "Algebra"), ("English", "Literature"), 
("Physics", "Kinematics"), ("History", "American Revolution");
