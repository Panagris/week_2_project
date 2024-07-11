import openai
import json


def run_quiz(CLIENT, subject: str, subtopic: str) -> dict:
    if subject == 'Math':
        return {"error": "Math quizzes are currently unsupported."}

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
                   f"with four options (A,B,C,D) focused on {subtopic}. "
                   f"The response should be packaged in a JSON file that "
                   f"follows this format {response_format_string}. Supply "
                   f"option choices (A, B, C, D) in the 'Question' field "
                   f"of the JSON, as dictated by the provided format. Always "
                   f"supply the options to the question in the 'Question' "
                   f"field. Ensure all questions are truly multiple choice. "
                   f"Supply the answer to each multiple choice question as "
                   f"demonstrated in the provided format sample. Strictly "
                   f"adhere to the Key names provided in the format "
                   f"for the returned JSON dictionary.")

    system_string = (f"You are a helpful study assistant for students that"
                     f"provides quiz questions and answers for a given subject"
                     f" and topic, responding with a JSON file adhering to "
                     f"this format {response_format_string}.")

    response = CLIENT.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_string},
            {"role": "user", "content": user_string},
        ]
    )

    content = response.choices[0].message['content'] \
        if isinstance(response.choices[0].message, dict) \
        else response.choices[0].message.content
    dictionary_quiz = json.loads(content)
    return dictionary_quiz
