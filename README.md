# README

Name: LearnMate AI
Problem to Solve: Students struggle with how to study effectively.
Who: Interfaces with human users.
Inputs: Text from the user.
Outputs: Text from the CHAT API
5 Steps: Get subject context from user, seed the CHAT, ask the user for questions, give to CHAT, parse CHAT response, return to user and ask if good response to prime CHAT
Biggest Risk: it doesn't work, and CHAT supplies bad answers (how do we ensure responses are good quality?)
Determine Success: user satisfaction. Ask the user if they received good responses.

### Dependencies
The openai module.
Python and pip(3) may through errors. Use these [instructions](https://stackoverflow.com/questions/75602063/pip-install-r-requirements-txt-is-failing-this-environment-is-externally-mana/75696359#75696359:~:text=This%20is%20due%20to%20your%20distribution%20adopting%20PEP%20668%20%E2%80%93%20Marking%20Python%20base%20environments%20as%20%E2%80%9Cexternally%20managed%E2%80%9D.) 
to create a virtual development environment for python.
```
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install <MODULE_TO_INSTALL>
```
The first CLI is needed only the first time; from then on, run ``source .venv/bin/activate`` to enter the python 
virtual environment. To leave the venv, run ``deactivate``.


## Brain Storm:
* Study buddy / tutor
* Anime recommender based on interests
* Choose Your Own Adventure
* Language translation
* Mental health / guided talk therapy 

## Questions
### Usefulness
* What problem is your project solving? - some people don't know how to study effectively
* For whom? - students
* Smallest piece that could be built? - Asking for the user for input
* Other aspects? - Generating sample questions, offering not just text-based input (files)
  If wanted to expand, maybe flashcards or another visual GUI

### Technology
* Data needed: subject, specific questions, unit name, what they already know/need help with
* Output: CHAT's response, but also an outline for how to study and the ability for user to ask more questions
* Inputs -> Outputs: rely on CHAT. Seed/prep chat with the scenario before asking user for info
* Neded tech: CHAT API, etc.