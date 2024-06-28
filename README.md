# README

Name: LearnMate AI

Problem to Solve: How can students who don't know where to begin studying 
efficiently prepare for exams with personalized and interactive 
study materials?

Inputs: Command-line text from the user.
Outputs: Text responses from the OpenAI API's generative AI model, often 
referred to as ChatGPT.

### Dependencies
The execution of the main() function within `gpt_tutor.py` is requires the
`openai` Python module as well as other modules. Follow the below command line 
operations to install these packages. Further, an [OpeanAI account](
https://platform.openai.com/docs/overview) is needed to receive an API key.
The program assumes that the API key stored as an environment variable.

```
pip install openai
```

The following are modules unrelated to the API but essential to the
function of the program: `sqlite3`, `os`, `json`, `sys`.

When developing locally, Python and pip(3) may through errors. 
Use these [instructions](
  https://stackoverflow.com/questions/75602063/pip-install-r-requirements-txt-is-failing-this-environment-is-externally-mana/75696359#75696359:~:text=This%20is%20due%20to%20your%20distribution%20adopting%20PEP%20668%20%E2%80%93%20Marking%20Python%20base%20environments%20as%20%E2%80%9Cexternally%20managed%E2%80%9D.) 
to create a virtual development environment for python.
```
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install <MODULE_TO_INSTALL>
```

The first command is needed only the first time to set up the environment.
From then on, run `source .venv/bin/activate` to enter the 
virtual environment. To leave the environment, execute `deactivate`.
