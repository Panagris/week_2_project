'''
This file handles the database, having functions that write and
read to the database that can be called by other files in the directory.
'''
import sqlite3 as sql
import sys
import os

DATABASE = "tutor.db"


def open_connection():
    try:
        connection = sql.connect(DATABASE)
        cursor = connection.cursor()

    except sql.Error as e:
        print(f"Error connecting to sqlite3 Platform: {e}")
        sys.exit(1)

    return connection, cursor


# Function to read and execute SQL commands from a file.
def execute_sql_file(file_path):
    connection, cursor = open_connection()

    with open(file_path, 'r') as sql_file:
        sql_commands = sql_file.read()
        cursor.executescript(sql_commands)
        connection.commit()


def create_database_if_empty():
    conn, cur = open_connection()
    if conn:
        cur.execute("SELECT COUNT(*) FROM sqlite_master \
                    WHERE type = 'table' AND name = 'users'")
        count = cur.fetchone()[0]

        if count == 0:
            execute_sql_file('populate_database.sql')
    conn.close()


def print_users() -> None:
    connection, cursor = open_connection()
    print("--- Registered Users ---\n")

    if connection:
        for row in cursor.execute("SELECT * FROM users"):
            print(f'ID: {row[0]}, Name: {row[1]}')
        connection.close()


def get_user_by_id(user_id) -> None:
    connection, cursor = open_connection()

    if connection:
        cursor.execute('SELECT name FROM users WHERE id = ?', (user_id,))
        name = cursor.fetchone()[0]
        connection.close()
        return name


def print_previous_subjects(user_id) -> None:
    connection, cursor = open_connection()

    if connection:
        cursor.execute('SELECT name FROM users WHERE id = ?', (user_id,))
        name = cursor.fetchone()[0]
        print(f"Previous classes for User: {name}")

        for row in cursor.execute("SELECT * FROM user_subjects \
                                    WHERE user_id = ?;", (user_id,)):
            print(f'ID: {row[0]}, Subject: {row[1]}')
        connection.close()


# Print all the subjects from the database.
def print_subjects() -> None:
    connection, cursor = open_connection()
    print("--- Available Subjects ---\n")

    if connection:
        for row in cursor.execute("SELECT * FROM subjects"):
            print(row[0])
        connection.close()


# Print all the study methods available.
def print_study_methods() -> None:
    connection, cursor = open_connection()
    print("--- Available Study Methods ---\n")

    if connection:
        for row in cursor.execute("SELECT * FROM study_methods"):
            print(row[0])
        connection.close()


def print_subtopics(subject: str) -> None:
    connection, cursor = open_connection()
    print(f"--- {subject} Subtopics ---\n")

    if connection:
        for row in cursor.execute("SELECT * FROM subtopics WHERE subject_name = ?", (subject,)):
            print(f'{row[0]}, {row[1]}')
        connection.close()


def add_user(user_name: str) -> int:
    connection, cursor = open_connection()

    if connection:
        cursor.execute("INSERT OR IGNORE INTO users (name) \
                    VALUES (?);", (user_name,))
        connection.commit()
        cursor.execute('SELECT id FROM users WHERE name = ?;', (user_name,))
        id = cursor.fetchone()[0]
        print(f"Added User: {user_name}")
        connection.close()
        return id

    return -1


def add_previous_subject(user_id: int, subject_name: str) -> None:
    connection, cursor = open_connection()

    if connection:
        cursor.execute("INSERT OR IGNORE INTO user_subjects \
                        (user_id, subject_name) \
                        VALUES (?, ?);", (user_id, subject_name))
        connection.commit()
        connection.close()


def clear_all_users() -> None:
    connection, cursor = open_connection()
    print("--- Clearing All Users ---\n")

    if connection:
        cursor.execute("DROP TABLE IF EXISTS users;")
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) DEFAULT NULL
            );
        """)
        connection.commit()
        print("All Users Cleared")
        connection.close()


# Populate table
if __name__ == "__main__":
    # Check that the database is not empty.
    create_database_if_empty()

    print_subjects()
    print_subtopics()
    print_study_methods()
    add_user("Beatrice")
    add_user("Mark")
    add_user("Jake")
    print_users()
    add_previous_subject(1, "Math")
    add_previous_subject(1, "English")
    add_previous_subject(1, "Computer Science")
    print_previous_subjects(1)

    clear_all_users()

    print_users()
