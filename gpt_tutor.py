import os
import openai
from openai import OpenAI
import database_handler as dbh

VALID_SUBJECTS = {dbh.get_subjects()}
VALID_SUBTOPICS = {"subject" : {}}
VALID_STUDY_METHODS = {}


def get_user_id() -> int:
    id = int(input("Please provide a USERID, or '-1' if you do not have one: "))

    if id == -1:
        # If they aren't a previous USER, ask for information.
        return create_user_ID()

    if id > (id_count := dbh.get_number_users()):
        print("That is currently not a valid ID.")

        while id > id_count and id != -1:
            id = int(input("Please provide a USERID, or '-1' if you do not have one: "))

            if int(id) == -1:
                return create_user_ID()

    name = dbh.get_user_by_id(id)
    print(f"Welcome back, {name}!")
    return id


# Ask the user for an existing USER ID, if available; -1 if N/A.
def create_user_ID() -> int:
    user_name = input("Please enter your name: ")
    user_id = dbh.add_user(user_name)
    return user_id

    

### TODO
# Ask the USER questions about themselves to prepare a USER for them in
# the database.
# This includes: subject, subtopics, grade / year, how they want to study.


# These should be options imported from a database so that the USER
# selects instead of providing plain text.
def get_study_session_info() -> None:
    dbh.print_subjects()
    subject_id = input("\nChoose a subject: ")

    dbh.print_subtopics(subject_id)
    subtopic_id = input("\nChoose a subtopic: ")

    dbh.print_study_methods()
    study_method_id = input("\nChoose a study method: ")
    return subject_id, subtopic_id, study_method_id



if __name__ == "__main__":
    user_id = get_user_id()
    subject_id, subtopic_id, study_method_id = get_study_session_info()

    # Set environment variables for the API key.
    my_api_key = os.environ.get('OPENAI_KEY')
    openai.api_key = my_api_key

    # Create an OpenAPI client using the key from our environment variable
    
    # client = OpenAI(api_key=my_api_key,)
    
    # # Seed / prepare ChatGPT with data about the user. Specify the model to
    # # use and the messages to send. Each run of the API is $0.01.
    # response = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "You are a helpful study assistant for students."},
    #         {"role": "user", "content": f"Give me an explanation for the subject {subject_id}, focusing on the subtopic {subtopic_id}."}
    #     ]
    # )

    # # Flesh things out, add the different options (Quiz, Explanation, etc.)
    # # Unit Tests - how do we do that?
    
    # # How to index into the response from ChatGPT.
    # print(response.choices[0].message.content.strip())

