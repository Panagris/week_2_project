import os
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
    id = int(input("Please provide a USERID, "
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
    print(f"Welcome back, {name}!")
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
def get_Chat_response(subject, subtopic, study_method):
    response = CLIENT.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful study \
            assistant for students."},
            {"role": "user", "content": f"Give me an {study_method} \
            for the subject {subject}, focusing on the subtopic \
            {subtopic}."}
        ]
    )
    return response


if __name__ == "__main__":
    user_id = get_user_id()
    subject_id, subtopic_id, study_method_id = get_study_session_info()
    # # Flesh things out, add the different options (Quiz, Explanation, etc.)
    response = get_Chat_response(subject_id, subtopic_id, study_method_id)

    # Index into the response from ChatGPT.
    print(response.choices[0].message.content.strip())
