# Seed / prepare ChatGPT with data about the user. Specify the model to
# use and the messages to send. Each run of the API is $0.01.
def run_explanation(CLIENT, subject: str, subtopic: str):
    system_string = ("You are a helpful study assistant for students "
                     "that provides summaries given a subject and a "
                     "subtopic about that subject.")

    user_string = (f"Generate a brief summary of {subject}, and then "
                   f"provide a thorough, detailed explanation of the "
                   f"following subtopic: {subtopic}. The response should"
                   f"be cover key points that may be included in a college"
                   f"-level lecture. It should also give ideas on how"
                   f" to more in-depthly explore the subtopic {subtopic}.")

    response = CLIENT.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_string},
            {"role": "user", "content": user_string}
        ]
    )
    return response
