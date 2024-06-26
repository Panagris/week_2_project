'''
This file handles the database, having functions that write and read to the database
that can be called by other files in the directory.
'''
import sqlite3 as sql
import sys
import os

DATABASE = "tutor.db"
def open_connection():
    try:
        connection = sql.connect(DATABASE)
        cursor = connection.cursor()
        # print(f"Successfully connected to {DATABASE}")

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

# Print all the subjects from the database.
def print_subject_list() -> None:
    connection, cursor = open_connection()

    if connection:
        for row in cursor.execute("SELECT * FROM subjects"):
            print(row[0])
        connection.close()

# Print all the study methods available.
def print_study_methods() -> None:
    connection, cursor = open_connection()

    if connection:
        for row in cursor.execute("SELECT * FROM study_methods"):
            print(row[0])
        connection.close()

def print_users() -> None:
    connection, cursor = open_connection()

    if connection:
        for row in cursor.execute("SELECT * FROM users"):
            print(f'ID: {row[0]}, Name: {row[1]}')
        connection.close()


def print_subtopics() -> None:
    connection, cursor = open_connection()

    if connection:
        for row in cursor.execute("SELECT * FROM subtopics"):
            print(f'{row[0]}, {row[1]}')
        connection.close()


def create_database_if_empty():
    conn, cur = open_connection()
    if conn:
        cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table' AND name = 'users'")
        count = cur.fetchone()[0]

        if count == 0:
            execute_sql_file('populate_database.sql')
    
    conn.close()

def add_user(user_name: str) -> None:
    connection, cursor = open_connection()
    input_string = f"INSERT OR IGNORE INTO users (name) \
                    VALUES ('{user_name}');"
    print(input_string)
    if connection:
        cursor.execute(input_string)
        connection.close()

def add_previous_subject(user_id: int, subject_name: str) -> None:
    connection, cursor = open_connection()
    input_string = f"INSERT INTO user_subjects (user_id, user_name) \
                    VALUES ({user_id}, '{subject_name}');"
    # print(input_string)

    if connection:
        cursor.execute(input_string)
        connection.close()

# Populate table
if __name__ == "__main__":
    # Check that the database is not empty.
    create_database_if_empty()
    
    # print_subject_list()
    # print_subtopics()
    # print_study_methods()
    add_user("Beatrice")
    add_user("Mark")
    add_user("Jake")
    # add_previous_subject(2, "Math")
    print_users()
    # INSERT INTO user_subjects (user_id, subject_name) VALUES (1, "Math"), (1, "English");