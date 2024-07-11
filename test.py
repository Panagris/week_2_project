import unittest
import sqlite3 as sql
from gpt_tutor import run_explanation
from flashcards import run_flashcards
from database_handler import open_connection, add_user, get_number_users


class TestGPTTutor(unittest.TestCase):
    def test_GPT_API_response(self):
        response = run_explanation("English", "Literature").object
        self.assertEqual(response, "chat.completion")


class TestFlashcards(unittest.TestCase):
    def test_run_flashcards(self):
        list_flashcards = run_flashcards("English", "Literature")
        self.assertIsInstance(list_flashcards, list)

        # Edge case type testing.
        self.assertIsInstance(list_flashcards[0], dict)
        self.assertIsInstance(list_flashcards[0]["Definition"], str)
        self.assertIsInstance(list_flashcards[0]["Term"], str)

        length = len(list_flashcards)

        self.assertIsInstance(list_flashcards[length-1], dict)
        self.assertIsInstance(list_flashcards[length-1]["Definition"], str)
        self.assertIsInstance(list_flashcards[length-1]["Term"], str)


class TestDBH(unittest.TestCase):

    def test_open_connection(self):
        connection, cursor = open_connection()
        self.assertIsInstance(connection, sql.Connection)
        self.assertIsInstance(cursor, sql.Cursor)

    def test_add_user(self):
        conn, cur = open_connection()
        if conn:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users_COPY (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(255) DEFAULT NULL
                );
            """)
            conn.commit()

            self.assertEqual(add_user("Jane Doe", "users_COPY"), 1)

            cur.execute("DROP TABLE users_COPY;")
            conn.commit()
            conn.close()

    def test_get_number_users(self):
        self.assertEqual(type(get_number_users()), int)

        conn, cur = open_connection()
        if conn:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users_COPY (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(255) DEFAULT NULL
                );""")
            conn.commit()

            cur.execute("""
                INSERT OR IGNORE INTO users_COPY (name)
                VALUES ('Jane Doe');
            """)
            conn.commit()

            self.assertEqual(get_number_users("users_COPY"), 1)

            cur.execute("DROP TABLE users_COPY;")
            conn.commit()

            conn.close()


if __name__ == '__main__':
    unittest.main()
