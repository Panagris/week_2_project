import json


# # Create an OpenAPI client using the key.
# MY_API_KEY = os.environ.get('OPENAI_KEY')
# openai.api_key = MY_API_KEY
# CLIENT = OpenAI(api_key=MY_API_KEY,)


# This function creates 15 flashcards based on the subject and subtopic
# provided by the user. The flashcards are created using the OpenAI API.
# The flashcards are returned as a list of dictionaries.
def run_flashcards(CLIENT, subject: str, subtopic: str) -> list:
    # The format string is used to create the JSON object.
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

    # print("\nStarting 15 Flashcards...\n")

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
    return list_flashcards
