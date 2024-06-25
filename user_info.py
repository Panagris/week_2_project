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
        print(f"Successfully connected to {DATABASE}")

    except sql.Error as e:
        print(f"Error connecting to sqlite3 Platform: {e}")
        sys.exit(1)
    
    return connection, cursor

# Function to read and execute SQL commands from a file
def execute_sql_file(file_path):
    connection, cursor = open_connection()

    with open(file_path, 'r') as sql_file:
        sql_commands = sql_file.read()
        cursor.executescript(sql_commands)
        connection.commit()


def print_subject_list() -> None:
    connection, cursor = open_connection()

    if connection:
        for row in cursor.execute("SELECT * FROM subjects"):
            print(row)
        connection.close()

def print_study_methods() -> None:
    connection = open_connection()
    if connection:
        connection.close()

def print_subtopics() -> None:
    connection = open_connection()
    if connection:
        connection.close()


# Populate table
execute_sql_file('user_data.sql')
print_subject_list()