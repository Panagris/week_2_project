import json

def run_quiz(CLIENT, subject: str, subtopic: str) -> dict:
    response_format_string = """
    {
        "Quiz": [
            {
                "Question": "Which of the following...
                A. Option...
                B. Option...
                C. Option...
                D. Option...",
                "Answer": "",
                "Answer Index": X,
                "Explanation": ""
            },
            {
                "Question": "What is...
                A. Option...
                B. Option...
                C. Option...
                D. Option...",
                "Answer": "",
                "Answer Index": X,
                "Explanation": ""
            }
        ]
    }
    """
    seed_user_string = (f"Generate a five-question multiple-choice {subject} "
                        f"quiz with four options (A,B,C,D) focused on "
                        f"{subtopic}. Include explanations for each answer. "
                        f"Return the quiz in a JSON format.")

    seed_response_format_dict = {
        "Quiz": [
            {
                "Question": """According to Newtons first law of motion, an
                            object at rest will remain at rest unless acted
                            upon by a(n):
                            A. frictional force
                            B. external force
                            C. gravitational force
                            D. magnetic force""",
                "Answer": "B. External force",
                "Answer Index": 2,
                "Explanation": "Newton's first law states that an object will remain at rest or in uniform motion unless acted upon by an external force."
            },
            {
                "Question": """Newtons second law of motion can be
                            mathematically represented as:
                            A. F = m a
                            B. F = m / a
                            C. F = a / m
                            D. F = m + a""",
                "Answer": "A. F= m a",
                "Answer Index": 1,
                "Explanation": "Newton's second law states that the force acting on an object is equal to the mass of that object times its acceleration."
            },
            {
                "Question": """When a rocket lifts off, the action force is the
                            force the rocket exerts on the gases to propel it
                            upward. The reaction force is the:
                            A. force of gravity pulling the rocket downward
                            B. force of air resistance slowing the rocket
                            C. force of the rocket propelling gases downward
                            D. force of magnetic attraction to Earth""",
                "Answer": "C. force of the rocket propelling gases downward",
                "Answer Index": 3,
                "Explanation": "According to Newton's third law, every action has an equal and opposite reaction. The rocket's action force on the gases results in an opposite reaction force propelling the rocket upwards."
            },
            {
                "Question": """According to Newton's third law of motion,
                            for every action, there is an equal and opposite
                            A. acceleration
                            B. force
                            C. momentum
                            D. velocity""",
                "Answer": "B. force",
                "Answer Index": 2,
                "Explanation": "Newton's third law states that for every action, there is an equal and opposite reaction force."
            },
            {
                "Question": """When a ball is thrown in the air, which of
                          Newton's laws explains why the ball comes back down
                          to the ground?
                          A. First law
                          B. Second law
                          C. Third law
                          D. Second and third laws""",
                "Answer": "A. First law",
                "Answer Index": 1,
                "Explanation": "Newton's first law explains that an object will stay in motion or at rest unless acted upon by an external force. Gravity acts as the external force that pulls the ball back to the ground."
            }
        ]
    }

    seed_response_JSON = json.dumps(seed_response_format_dict)

    user_input_string = (f"Generate a five-question multiple-choice {subject}"
                         f" quiz with four options (A,B,C,D) focused on "
                         f"{subtopic}. Include explanations for each answer. "
                         f"Return the quiz in a JSON format.")

    system_string = (f"You are a helpful study assistant for students that "
                     f"provides quiz questions, answers, answer indices, "
                     f"and explanations for a given "
                     f"subject and topic, responding with a JSON file "
                     f"adhering to this format: {response_format_string}."
                     f"Supply option choices (A, B, C, D) in the Question "
                     f"field, the answer in the Answer field, "
                     f"an integer value in the Answer Index field "
                     f"to indicate the correct answer. The index should be 1 "
                     f"for A, 2 for B, 3 for C, and 4 for D. Provide an explanation in the Explanation field.")

    response = CLIENT.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_string},
            {"role": "user", "content": seed_user_string},
            {"role": "assistant", "content": seed_response_JSON},
            {"role": "user", "content": user_input_string},
        ]
    )

    content = json.loads(response.choices[0].message.content)

    return content
