import os
import json
import openai
from openai import OpenAI
import database_handler as dbh

VALID_SUBJECTS = dbh.get_subjects()
VALID_SUBTOPICS = {subject: dbh.get_subtopics(subject)
                   for subject in VALID_SUBJECTS}
VALID_STUDY_METHODS = dbh.get_study_methods()

# Set environment variables for the API key.
MY_API_KEY = os.environ.get('OPENAI_KEY')
openai.api_key = MY_API_KEY
# Create an OpenAPI client using the key.
CLIENT = OpenAI(api_key=MY_API_KEY,)


def get_user_id() -> int:
    id = int(input("Please provide a User ID Number, "
                   "or '-1' if you do not have one: "))

    if id == -1:
        # If they aren't a previous USER, ask for information.
        return create_user_ID()

    if id > (id_count := dbh.get_number_users()):
        print("That is currently not a valid ID.")

        while id > id_count and id != -1:
            id = int(input("Please provide a USERID, "
                           "or '-1' if you do not have one: "))

            if int(id) == -1:
                return create_user_ID()

    name = dbh.get_user_by_id(id)
    print(f"\nWelcome back, {name}!")
    return id


# Ask the user for an existing USER ID, if available; -1 if N/A.
def create_user_ID() -> int:
    user_id = -1
    user_name = input("Please enter your name: ").strip()

    if not user_name:
        print("Error: User name cannot be empty.")
        return -1

    user_id = dbh.add_user(user_name)
    return user_id


# Ask the USER questions about themselves to prepare a USER for them in
# the database.
# This includes: subject, subtopics, grade / year, how they want to study.
# These should be options imported from a database so that the USER
# selects instead of providing plain text.
def get_study_session_info() -> tuple:
    while True:
        dbh.print_subjects()
        subject_id = input("\nChoose a subject: ").strip()

        if subject_id not in VALID_SUBJECTS:
            print("Error: Invalid subject. Please choose from the "
                  "available subjects.")
            continue

        while True:
            dbh.print_subtopics(subject_id)
            subtopic_id = input("\nChoose a subtopic: ").strip()

            if subtopic_id in VALID_SUBTOPICS.get(subject_id, []):
                break  # Break the subtopic selection loop if valid
            else:
                print("Error: Invalid subtopic. "
                      "Please choose from the available subtopics.")

        while True:
            dbh.print_study_methods()
            study_method_id = input("\nChoose a study method: ").strip()

            if study_method_id in VALID_STUDY_METHODS:
                break  # Break the study method selection loop if valid
            else:
                print("Error: Invalid study method. "
                      "Please choose from the available study methods.")

        return subject_id, subtopic_id, study_method_id


# Seed / prepare ChatGPT with data about the user. Specify the model to
# use and the messages to send. Each run of the API is $0.01.
def run_explanation(subject, subtopic):
    response = CLIENT.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful study \
            assistant for students."},
            {"role": "user", "content": f"Give me an explanation \
            for the subject {subject}, focusing on the subtopic \
            {subtopic}."}
        ]
    )
    return response


def run_quiz(subject, subtopic):
    response_format_string = """
        {
            "Quiz": [
                {
                    "Question": "",
                    "Answer": "The Correct Answer is: "
                },
                {
                    "Question": "",
                    "Answer": "The Correct Answer is: "
                }
                ]
        }
        """
    user_string = (f"Generate a {subject} five-question multiple-choice quiz "
                   f"with four options (A,B,C,D) focused on {subtopic}."
                   f"The response should be packaged in a JSON file that "
                   f"follows this format {response_format_string}. Supply "
                   f"the answer to each multiple choice question as "
                   f"demonstrated in the provided format sample. Strictly"
                   f" adhere to the Key names provided in the format "
                   f"for the returned JSON dictionary.")

    print("Starting Quiz...\n")

    response = CLIENT.chat.completions.create(
        model="gpt-3.5-turbo",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful study\
             assistant for students."},
            {"role": "user", "content": user_string},
        ]
    )

    dictionary_quiz = json.loads(response.choices[0].message.content)
    quiz_key = list(dictionary_quiz.keys())[0]
    list_quiz = dictionary_quiz[quiz_key]

    for question_num, quiz_question in enumerate(list_quiz, start=1):
        question_key = list(quiz_question.keys())[0]
        answer_key = list(quiz_question.keys())[1]

        # print(f"Question {question_num}: {quiz_question[question_key]}")
        print(f"Question {question_num}: {quiz_question[question_key]}")
        user_answer = input("\nEnter your response to see the"
                            " correct answer: ")

        if user_answer == 'STOP':
            return
        print(quiz_question[answer_key], "\n")

    print("Quiz completed!\n")


def run_flashcards(subject, subtopic):
    format_string = """
    {
        "flashcards": [
            {
                "Definition": "",
                "Term": ""
            },
            {
                "Definition": "",
                "Term": ""
            }
            ]
    }
    """

    user_field = (f"Package 15 flashcards about the subtopic {subtopic} "
                  f"about the subject {subject} and package them as a "
                  f"JSON file that follows the format {format_string}, "
                  f"and keep the name of the term out of the Definition "
                  f"field. Given a definition, I will be able to supply the "
                  f"vocabulary word.")

    response = CLIENT.chat.completions.create(
        model="gpt-3.5-turbo",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful study assistant \
            for students designed to output JSON."},
            {"role": "user", "content": user_field}
        ]
    )

    dictionary_flashcards = json.loads(response.choices[0].message.content)
    flashcard_key = list(dictionary_flashcards.keys())[0]
    list_flashcards = dictionary_flashcards[flashcard_key]

    for flashcard in list_flashcards:
        definition_key, term_key = list(quiz_question.keys())

        print(flashcard[definition_key])
        user_answer = input("\tWhat is the term? Or, enter 'STOP' to quit: ")

        if user_answer == 'STOP':
            return
        print("The correct term was: ", flashcard[term_key], "\n")


if __name__ == "__main__":
    user_id = get_user_id()
    do_again = True

    while do_again:
        subject_id, subtopic_id, study_method_id = get_study_session_info()

        if study_method_id == 'Quiz':
            run_quiz(subject_id, subtopic_id)
        elif study_method_id == 'Flashcards':
            run_flashcards(subject_id, subtopic_id)
        elif study_method_id == 'Explanation':
            response = run_explanation(subject_id, subtopic_id)
            print(response.choices[0].message.content.strip())

        while True:
            response = input("\nWould you like to do this again? (Y/N) ")
            if response in ['N', 'n']:
                do_again = False
                break
            elif response in ['Y', 'y']:
                break
