import os
import openai
from openai import OpenAI
import user_info


# Set environment variables for the API key.
my_api_key = os.environ.get('OPENAI_KEY')
openai.api_key = my_api_key

# Ask the user for an existing USER ID, if available; -1 if N/A.
def get_user_ID() -> int:
    id = int(input("Please provide a USERID, or '-1' if you do not\
     have one: "))

    # If they aren't a previous USER, ask for information.
    if id == -1:
        id = create_user_ID()
        print(f"The following ID has been generated for you: {id}")
    return id

### TODO
# Ask the USER questions about themselves to prepare a USER for them in
# the database.
# This includes: subject, subtopics, grade / year, how they want to study.
def create_user_ID() -> int:
    gen_id = 1
    return gen_id

# These should be options imported from a database so that the USER
# selects instead of providing plain text.
def get_study_session_info() -> None:
    print_subject_list()  ### TODO

    subject = int(input("What subject would you like to study? \
                        Pass by ID #: \n"))

    print_subtopics(subject)  ### TODO

    subtopic = int(input("What subtopic would you like to focus on? \
                         Pass by ID #: \n"))
    
    print_study_methods()

    # Options: Q&A (Quiz), Fill-in-the-Blank, Explanations, GUI-less Flashcards.
    study_method = int(input("How would you prefer to study? \
                             Pass by ID #: \n"))
    
    return subject, subtopic, study_method


if __name__ == "__main__":
    #user_id = get_user_ID();

    #subject, subtopic, study_method = get_study_session_info()

    # Create an OpenAPI client using the key from our environment variable
    client = OpenAI(api_key=my_api_key,)
    

    # Seed / prepare ChatGPT with data about the user. Specify the model to
    # use and the messages to send. Each run of the API is $0.01.
    '''
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
                # System: tell Chat who it is and how it should behave
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"}, # The actual question
                # Provides sample feedback, also a means to store previous responses.
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played?"} 
            ]
    )
    '''
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful study assistant for students"},
            {"role": "user", "content": "Give me an explanation for Computer Science focusing on Djikstras"},
            #{"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            
        ]
    )
    # How to index into the response from ChatGPT.
    print(response.choices[0].message.content.strip())

