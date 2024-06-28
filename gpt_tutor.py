import os
import json
import openai
import sys
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
    id = input("Please provide a User ID Number, "
               "or '-1' if you do not have one: ")
    try:
        id = int(id)
    except ValueError:
        print("\nAn invalid value for a user ID was provided. Please run "
              "the program again with an integer value for a user ID.")
        print("\nTerminating Program...\n")
        sys.exit(0)

    if id == -1:
        # If they aren't a previous USER, ask for information.
        return create_user_ID()

    if id not in range(1, id_count := dbh.get_number_users()):
        print("That is currently not a valid ID.")

        while id not in range(1, id_count) and id != -1:
            id = int(input("Please provide a USERID, "
                           "or '-1' if you do not have one: "))

            if int(id) == -1:
                return create_user_ID()

    name = dbh.get_user_by_id(id)
    print(f"\nWelcome back, {name}!")
    return id


# Ask the user for an existing USER ID, if available; -1 if N/A.
def create_user_ID() -> int:
    user_name = input("Please enter your name: ").strip()

    while not user_name:
        print("\nError: User name cannot be empty.\n")
        user_name = input("Please enter your name: ").strip()

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
            print("\nError: Invalid subject. Please choose from the "
                  "available subjects.")
            continue

        while True:
            dbh.print_subtopics(subject_id)
            subtopic_id = input("\nChoose a subtopic: ").strip()

            if subtopic_id in VALID_SUBTOPICS.get(subject_id, []):
                break  # Break the subtopic selection loop if valid
            else:
                print("\nError: Invalid subtopic. "
                      "Please choose from the available subtopics.")

        while True:
            dbh.print_study_methods()
            study_method_id = input("\nChoose a study method: ").strip()

            if study_method_id in VALID_STUDY_METHODS:
                break  # Break the study method selection loop if valid
            else:
                print("\nError: Invalid study method. "
                      "Please choose from the available study methods.")

        return subject_id, subtopic_id, study_method_id


# Seed / prepare ChatGPT with data about the user. Specify the model to
# use and the messages to send. Each run of the API is $0.01.
def run_explanation(subject, subtopic):
    print('\nGenerating Explanation Summary...\n')

    system_string = (f"You are a helpful study assistant for students "
                     f"that provides summaries given a subject and a "
                     f"subtopic about that subject.")

    user_string = (f"Generate a brief summary of {subject}, and then "
                   f"provide a thorough, detailed explanation of the "
                   f"following subtopic: {subtopic}. The response should"
                   f"be cover key points that may be included in a college"
                   f"-level lecture. It should also give ideas on how"
                   f" to more in-depthly explore the subtopic {subtopic}.")

    response = CLIENT.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_string},
            {"role": "user", "content": user_string}
        ]
    )
    return response


def run_quiz(subject, subtopic):
    if subject == 'Math':
        print('Unfortunately, current generative models are unable to '
              'accurately supply correct, mathematical answers. Please '
              'try again later!')
        return

    response_format_string = """
        {
            "Quiz": [
                {
                    "Question": "Which of the following...
                    A. Option...
                    B. Option...
                    C. Option...
                    D. Option...",
                    "Answer": "The Correct Answer is: "
                },
                {
                    "Question": "What is...
                    A. Option...
                    B. Option...
                    C. Option...
                    D. Option...",
                    "Answer": "The Correct Answer is: "
                }
                ]
        }
        """
    user_string = (f"Generate a {subject} five-question multiple-choice quiz "
                   f"with four options (A,B,C,D) focused on {subtopic}."
                   f"The response should be packaged in a JSON file that "
                   f"follows this format {response_format_string}. Supply "
                   f"option choices (A, B, C, D) in the 'Question' field"
                   f"of the JSON, as dictated by the provided format. Always "
                   f"supply the options to the question in the 'Question' "
                   f"field. Ensure all questions are truly multiple choice. "
                   f"Supply the answer to each multiple choice question as "
                   f"demonstrated in the provided format sample. Strictly"
                   f" adhere to the Key names provided in the format "
                   f"for the returned JSON dictionary.")

    system_string = (f"You are a helpful study assistant for students that"
                     f"provides quiz questions and answers for a given subject"
                     f" and topic, responding with a JSON file adhering to "
                     f"this format {response_format_string}.")

    print("\nStarting Quiz...\n")

    response = CLIENT.chat.completions.create(
        model="gpt-3.5-turbo",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_string},
            {"role": "user", "content": user_string},
        ]
    )

    dictionary_quiz = json.loads(response.choices[0].message.content)
    quiz_key = list(dictionary_quiz.keys())[0]
    list_quiz = dictionary_quiz[quiz_key]

    for question_num, quiz_question in enumerate(list_quiz, start=1):
        question_key = list(quiz_question.keys())[0]
        answer_key = list(quiz_question.keys())[1]

        print(f"Question {question_num}: {quiz_question[question_key]}")
        user_answer = input("\nEnter your response to see the"
                            " correct answer, or 'STOP' to quit: ")

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

    print("\nStarting 15 Flashcards...\n")

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

    for card_num, flashcard in enumerate(list_flashcards, start=1):
        definition_key, term_key = list(flashcard.keys())

        print(f'Definition {card_num}: {flashcard[definition_key]}')
        user_answer = input("\nWhat is the term? Or, enter 'STOP' to quit: ")

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
            response = input("\nWould you like to continue studying? (Y/N) ")
            if response in ['N', 'n']:
                do_again = False
                break
            elif response in ['Y', 'y']:
                break
