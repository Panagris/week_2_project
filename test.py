import unittest
from main import CLIENT
from gpt_tutor import run_explanation
from flashcards import run_flashcards
from quiz import run_quiz


class TestGPTTutor(unittest.TestCase):
    def test_GPT_API_response(self):
        response = run_explanation(CLIENT, "English", "Literature").object
        self.assertEqual(response, "chat.completion")


class TestFlashcards(unittest.TestCase):
    def test_run_flashcards(self):
        list_flashcards = run_flashcards(CLIENT, "English", "Literature")
        self.assertIsInstance(list_flashcards, list)

        # Edge case type testing.
        self.assertIsInstance(list_flashcards[0], dict)
        self.assertIsInstance(list_flashcards[0]["Definition"], str)
        self.assertIsInstance(list_flashcards[0]["Term"], str)

        length = len(list_flashcards)

        self.assertIsInstance(list_flashcards[length-1], dict)
        self.assertIsInstance(list_flashcards[length-1]["Definition"], str)
        self.assertIsInstance(list_flashcards[length-1]["Term"], str)


class TestQuiz(unittest.TestCase):
    def test_run_quiz(self):
        quiz_data = run_quiz(CLIENT, "English", "Literature")
        list_quiz = quiz_data["Quiz"]
        self.assertIsInstance(quiz_data, dict)

        # Edge case type testing.
        self.assertIsInstance(list_quiz[0], dict)
        self.assertIsInstance(list_quiz[0]["Question"], str)
        self.assertIsInstance(list_quiz[0]["Answer"], str)

        length = len(list_quiz)

        self.assertIsInstance(list_quiz[length-1], dict)
        self.assertIsInstance(list_quiz[length-1]["Question"], str)
        self.assertIsInstance(list_quiz[length-1]["Answer"], str)


if __name__ == '__main__':
    unittest.main()
