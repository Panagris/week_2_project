import os
import openai
from openai import OpenAI
import database_handler as dbh


# Set environment variables for the API key.
my_api_key = os.environ.get('OPENAI_KEY')
openai.api_key = my_api_key

# Ask the user for an existing USER ID, if available; -1 if N/A.
def create_user_ID() -> int:
    id = int(input("Please provide a USERID, or '-1' if you do not\
     have one: "))
    # If they aren't a previous USER, ask for information.
    if id == -1:
        user_id = create_user_ID()
        user_name = input("Please enter your name: ")
        dbh.add_user(user_name)
    return user_id

    

### TODO
# Ask the USER questions about themselves to prepare a USER for them in
# the database.
# This includes: subject, subtopics, grade / year, how they want to study.
def create_user_name() -> int:
    user_name = input("Please enter your name: ")
    user_id = dbh.add_user(user_name)
    return user_id

# These should be options imported from a database so that the USER
# selects instead of providing plain text.
def get_study_session_info() -> None:
    dbh.print_subject_list()
    subject_id = int(input("Choose a subject by ID: "))
    dbh.print_subtopics(subject_id)  
    subtopic_id = int(input("Choose a subtopic by ID: "))
    dbh.print_study_methods()
    study_method_id = int(input("Choose a study method by ID: "))
    return subject_id, subtopic_id, study_method_id



if __name__ == "__main__":
    user_id = create_user_ID()
    subject_id, subtopic_id, study_method_id = get_study_session_info()

    # Create an OpenAPI client using the key from our environment variable
    client = OpenAI(api_key=my_api_key,)
    

    # Seed / prepare ChatGPT with data about the user. Specify the model to
    # use and the messages to send. Each run of the API is $0.01.

    response = client.chat_completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful study assistant for students."},
            {"role": "user", "content": f"Give me an explanation for the subject with ID {subject_id}, focusing on the subtopic with ID {subtopic_id}."}
        ]
    )
    # How to index into the response from ChatGPT.
    print(response.choices[0].message.content.strip())

