import json


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
    # The user_field is the prompt that is sent to the OpenAI API.
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
    # The response is a JSON object that contains the flashcards. The list of
    # flashcards is stored in a dictionary with the key being the term and
    # the value being the definition.
    dictionary_flashcards = json.loads(response.choices[0].message.content)
    flashcard_key = list(dictionary_flashcards.keys())[0]
    list_flashcards = dictionary_flashcards[flashcard_key]
    return list_flashcards
