# TODO: IMPORT NECESSARY FUNCTIONS FROM GPT_TUTOR


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
