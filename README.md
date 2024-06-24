# README

Name: LearnMate AI
Problem to Solve: Students struggle with how to study effectively.
Who: Interfaces with human users.
Inputs: Text from the user.
Outputs: Text from the CHAT API
5 Steps: Get subject context from user, seed the CHAT, ask the user for questions, give to CHAT, parse CHAT response, return to user and ask if good response to prime CHAT
Biggest Risk: it doesn't work, and CHAT supplies bad answers (how do we ensure responses are good quality?)
Determine Success: user satisfaction. Ask the user if they received good responses.

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