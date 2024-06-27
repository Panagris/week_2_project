'''
This file handles the database, having functions that write and
read to the database that can be called by other files in the directory.
'''
import sqlite3 as sql
import sys
import os

DATABASE = "tutor.db"


def open_connection(db=DATABASE):
    try:
        connection = sql.connect(db)
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
    print("\n--- Registered Users ---\n")

    if connection:
        for row in cursor.execute("SELECT * FROM users"):
            print(f'ID: {row[0]}, Name: {row[1]}')
        connection.close()


def get_user_by_id(user_id) -> None:
    connection, cursor = open_connection()

    if connection:
        cursor.execute('SELECT name FROM users WHERE id = ?', (user_id,))
        response = cursor.fetchone()

        if response:
            name = response[0]
        else:
            print("That was not a valid User ID.")
        connection.close()
        return name


def get_number_users(table="users") -> int:
    connection, cursor = open_connection()
    if connection:
        cursor.execute(f""" SELECT COUNT(*)
                        FROM {table}; """)
        if response := cursor.fetchone():
            return response[0]
    return -1


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


def get_subjects() -> list:
    connection, cursor = open_connection()
    subject_set = []
    if connection:
        for row in cursor.execute("SELECT * FROM subjects"):
            subject_set.append(row[0])
        connection.close()
    return subject_set


# Print all the subjects from the database.
def print_subjects() -> None:
    print("\n--- Available Subjects ---\n")
    for subject in get_subjects():
        print(subject)


def get_study_methods() -> list:
    connection, cursor = open_connection()
    study_methods = []
    if connection:
        for row in cursor.execute("SELECT * FROM study_methods"):
            study_methods.append(row[0])
        connection.close()
    return study_methods


# Print all the study methods available.
def print_study_methods() -> None:
    print("\n--- Available Study Methods ---\n")

    for study_method in get_study_methods():
        print(study_method)


def get_subtopics(subject: str) -> list:
    connection, cursor = open_connection()
    subtopics = []
    if connection:
        for row in cursor.execute("""SELECT * FROM subtopics
                                    WHERE subject_name = ?""", (subject,)):
            subtopics.append(row[1])
        connection.close()
    return subtopics


def print_subtopics(subject: str) -> None:
    print(f"\n--- {subject} Subtopics ---\n")

    for subtopic in get_subtopics(subject):
        print(f'\t{subtopic}')


def add_user(user_name: str, user_table="users") -> int:
    connection, cursor = open_connection()

    if connection:
        cursor.execute(f"INSERT OR IGNORE INTO {user_table} (name) \
                    VALUES (?);", (user_name,))
        connection.commit()
        cursor.execute(f'SELECT id FROM {user_table} \
                        WHERE name = ?;', (user_name,))

        id = -1  # Error Return Value.
        if response := cursor.fetchone():
            id = response[0]
            print(f"Added User: {user_name}. Your ID is: {id}")
        else:
            print(f"""Apologies. An error occurred adding User {user_name}.
                    Try again later.""")

        connection.close()
        return id


def add_previous_subject(user_id: int, subject_name: str) -> None:
    connection, cursor = open_connection()

    if connection:
        cursor.execute("INSERT OR IGNORE INTO user_subjects \
                        (user_id, subject_name) \
                        VALUES (?, ?);", (user_id, subject_name))
        connection.commit()
        connection.close()


def add_subtopic(subject: str, subtopic: str) -> None:
    connection, cursor = open_connection()

    if connection:
        cursor.execute("""INSERT OR IGNORE INTO subtopics
                        (subject_name, subtopic)
                        VALUES (?, ?);""", (subject, subtopic))
        connection.commit()

        # print(f"Added Subtopic: {subtopic}. View changes below. \n")
        # print_subtopics(subject)
        connection.close()


def clear_all_users() -> None:
    connection, cursor = open_connection()
    print("\n--- Clearing All Users ---\n")

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
    # create_database_if_empty()

    # print_subjects()
    # print_subtopics("Math")
    # print_study_methods()
    # add_user("Beatrice")
    # add_user("Mark")
    # add_user("Jake")
    # print_users()
    # add_previous_subject(1, "Math")
    # add_previous_subject(1, "English")
    # add_previous_subject(1, "Computer Science")
    # print_previous_subjects(1)

    # clear_all_users()
    # print(f"The number of users: {get_number_users()}")

    add_subtopic("Math", "Calculus")
