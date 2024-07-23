# LearnMateAI
Students are often overwhelmed when trying to study and prepare for exams.
Many have trouble concentrating on their studies, retaining material, or
just lack effective study habits.

We introduce LearnMateAI to address these problems. LearnMateAI is an online,
interactive study site that allows students to study various common academic
subjects. It offers personalized and dynamic AI-powered study methods including
Quizzes and Flashcards.

To get started with [LearnMateAI](https://learnmateai.pythonanywhere.com 'LearnMateAI'),
sign up with a username and password on the site. After logging in, you
will have access to LearnMateAI's exclusive
[Quizzes](https://learnmateai.pythonanywhere.com/quiz 'Quizzes') and
[Flashcards](https://learnmateai.pythonanywhere.com/flashcards 'Flashcards')!

## Getting Started
To get started developing, it is recommended to have the latest version of
Python3 installed on your system. Clone our Github repository into a known
location on your system and navigate to the project directory.

### Dependencies
LearnMateAI utilizes SQLite3. Ensure this is installed on your system.

LearnMateAI requires several Python Modules, including the `openai` module.
Run the command below to ensure these modules are installed on your system.

```
pip3 install -r requirements.txt
```

Furthermore, LearnMateAI requires an
[OpenAI Key](https://platform.openai.com/docs/overview 'OpenAI Docs') and a
[Flask Secret Key](https://flask.palletsprojects.com/en/2.3.x/config/ 'Flask Configuration').
An OpenAI account is needed to recieve an OpenAI Key.
For security purposes, these 2 must be stored as environment variables on your system.
Reach out to us for these keys if needed.

When developing locally, you might need to set up a virtual development environment
for Python. Follow these [instructions](
  https://stackoverflow.com/questions/75602063/pip-install-r-requirements-txt-is-failing-this-environment-is-externally-mana/75696359#75696359:~:text=This%20is%20due%20to%20your%20distribution%20adopting%20PEP%20668%20%E2%80%93%20Marking%20Python%20base%20environments%20as%20%E2%80%9Cexternally%20managed%E2%80%9D.
) if necessary.

Example:
```
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

The first command is needed only the first time to set up the environment.
From then on, run `source .venv/bin/activate` to enter the 
virtual environment. To leave the environment, execute `deactivate`.

## Testing the Project
Within the project directory, run
```
python3 main.py
```

This will configure and run the server. You should be able to access the site
on your local machine. Read main's output for more information on how
you can access the site locally.
