from openai import OpenAI
import json


def run_quiz(CLIENT: OpenAI, subject: str, subtopic: str) -> None:
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
