from flask import Flask, render_template, url_for, flash, redirect, \
    request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import TypeDecorator, VARCHAR
from flask_behind_proxy import FlaskBehindProxy
from flask_login import UserMixin, LoginManager, login_user, \
    login_required, logout_user, current_user
import openai
from openai import OpenAI
import os
import git
import json
from time import sleep
from flashcards import run_flashcards
from quiz import run_quiz
from scoring import SCORE_TO_XP, xp_level


# The SQLAlchemy object is created and used to interact with the database.
db = SQLAlchemy()

# SUBJECT_SUBTOPIC_DICT is a dictionary that contains the subjects as keys
# and the subtopics as values.
SUBJECT_SUBTOPIC_DICT = {
    "Physics": [
        "Mechanics",
        "Electromagnetism",
        "Thermodynamics",
        "Optics",
        "Modern Physics",
        "Astrophysics"
    ],
    "Chemistry": [
        "Organic Chemistry",
        "Inorganic Chemistry",
        "Physical Chemistry",
        "Analytical Chemistry",
        "Biochemistry",
        "Environmental Chemistry"
    ],
    "Biology": [
        "Cell Biology",
        "Genetics",
        "Ecology",
        "Evolution",
        "Human Anatomy and Physiology",
        "Microbiology"
    ],
    "Computer-Science": [
        "Data Structures and Sorting Algorithms",
        "Software Engineering",
        "Artificial Intelligence",
        "Databases",
        "Computer Networks",
        "Cybersecurity"
    ],
    "History": [
        "Ancient Civilizations",
        "Medieval History",
        "Modern History",
        "American History",
        "World History",
        "Cultural History"
    ],
    "Economics": [
        "Microeconomics",
        "Macroeconomics",
        "International Economics",
        "Development Economics",
        "Behavioral Economics",
        "Environmental Economics"
    ]
}


# Used when Signing in and Signing up
class User(UserMixin, db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))  # Stores only hashed passwords
    xp = db.Column(db.Integer)
    xp_level = db.Column(db.String(100))

    # Each user will have multiple flashcards they will want to access
    flashcards = db.relationship("Flashcards", backref="user")

    # Each user will have multiple quiz results they will want to access
    quiz_results = db.relationship('QuizResult', backref='user')

    # String representation of a user for debugging purposes
    def __repr__(self):
        return f'<User: {self.username} :: {self.xp} XP ({self.xp_level})>'


# Used to store the flashcards in the database
# Define a custom column type that inherits from TypeDecorator. TypeDecorator
# is for user-defined types, helping to marshall data to/from the DB.
# Marshlling transforms the memory representation of an object to a data
# format suitable for passing into the relational DB.
class JSONEncodedDict(TypeDecorator):
    """Enables JSON storage by encoding and decoding on the fly."""
    impl = VARCHAR
    # Implement the process_bind_param method to serialize data to JSON format
    # when saving to the database.

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        return json.dumps(value)

    # Process_result_value method to deserialize JSON back into Python data
    # when loading from the database.
    def process_result_value(self, value, dialect):
        if value is None:
            return value
        return json.loads(value)


# Update the Flashcards model
class Flashcards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100))
    subtopic = db.Column(db.String(100))
    missed_flashcards = db.Column(JSONEncodedDict)
    correct_flashcards = db.Column(JSONEncodedDict)

    # Represents the user that generated these flashcards.
    # Links back to User table.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # String representation of a user for debugging purposes
    def __repr__(self):
        return f'<Subject: {self.subject}, Subtopic: {self.subtopic}' \
            f' :: Length Correct: {len(self.correct_flashcards)}' \
            f' :: Length Missed: {len(self.missed_flashcards)}>'


# Used for storing prior quiz results
class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)  # The time the quiz was completed
    subject = db.Column(db.String(100))
    subtopic = db.Column(db.String(100))
    num_correct = db.Column(db.Integer)

    # Represents the user that took this quiz; links back to User table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # String representation of a quiz result for debugging purposes
    def __repr__(self):
        return f"<{self.user.username}'s Quiz Result :: " \
            f"{self.subtopic} ({self.subject}) : {self.num_correct} / 5>"


# The OpenAI API key is stored in an environment variable and used to
# authenticate the OpenAI API, stored in the CLIENT constant.
MY_API_KEY = os.environ.get('OPENAI_KEY')
openai.api_key = MY_API_KEY
CLIENT = OpenAI(api_key=MY_API_KEY,)

# Basic App Configuration
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
proxied = FlaskBehindProxy(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tutor.db'

# Initialize the database if it doesn't already exist
db.init_app(app)
with app.app_context():
    db.create_all()

# Initialize the Login Manager
login_manager = LoginManager()
login_manager.login_view = "signin"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table,
    # use it in the query for the user
    return User.query.get(int(user_id))


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


# This route prompts the user for a subject and subtopic before actually
# displaying the flashcards.
@app.route("/flashcards")
@login_required
def flashcards():
    return render_template('topics.html', subjects=SUBJECT_SUBTOPIC_DICT,
                           subject_dictionary=SUBJECT_SUBTOPIC_DICT)


# This route is used to display the flashcards page with the subject and
# subtopic selected by the user. The subject and subtopic are passed as
# parameters in the URL from the previous form submission.
@app.route("/flashcards", methods=['POST'])
@login_required
def flashcards_post():
    subject = request.form.get('subject_selection')
    subtopic = request.form.get('subtopic_selection')
    # TODO Change render_temp() to include ID of the flashcard deck
    return render_template('flashcards.html', subject=subject,
                           subtopic=subtopic, missed_flashcards=[],
                           correct_flashcards=[])


# This route is used to generate the flashcards based on the subject and
# subtopic selected by the user. The subject and subtopic are passed as
# parameters to the URL from a AJAX request from the JS script
# embedded in /templates/flashcards.html.
@app.route("/get-cards", methods=['POST'])
def get_cards():
    data = request.json
    subject = data.get("subject")
    subtopic = data.get("subtopic")
    flashcards = run_flashcards(CLIENT, subject, subtopic)

    flashcards_db = Flashcards(
        subject=subject,
        subtopic=subtopic,
        missed_flashcards=flashcards,
        correct_flashcards=[],
        user=current_user
    )
    db.session.add(flashcards_db)
    db.session.commit()

    deck_id = flashcards_db.id
    flashcards.append(deck_id)

    return jsonify(flashcards)


# This route is used to generate dummy flashcards for testing purposes.
@app.route("/dummy-get-cards", methods=['POST'])
def dummy_get_cards():
    flashcards = [
        {"Definition": "Definition 1", "Term": "Term 1"},
        {"Definition": "Definition 2", "Term": "Term 2"},
        {"Definition": "Definition 3", "Term": "Term 3"},
        {"Definition": "Definition 4", "Term": "Term 4"},
    ]

    flashcards_db = Flashcards(
        subject="Test",
        subtopic="Test",
        missed_flashcards=flashcards,
        correct_flashcards=[],
        user=current_user
    )
    db.session.add(flashcards_db)
    db.session.commit()

    deck_id = flashcards_db.id
    flashcards.append(deck_id)
    sleep(2)  # Simulate waiting for an API response.
    return jsonify(flashcards)


@app.route("/save-cards", methods=['POST'])
def save_flashcards():
    data = request.json
    deck_id = data.get("deckId")
    missed_flashcards = data.get("missedFlashcards")
    correct_flashcards = data.get("correctFlashcards")

    flashcard_deck = Flashcards.query.filter_by(id=deck_id).first()
    flashcard_deck.missed_flashcards = missed_flashcards
    flashcard_deck.correct_flashcards = correct_flashcards

    db.session.commit()
    flash('Flashcards saved successfully!', 'info')
    return url_for("saved_flashcards")


@app.route("/load-cards", methods=['POST'])
@login_required
def load_flashcards():
    # Load flashcards from Database
    deck_id = int(request.form.get("deckId"))

    flashcard_deck = Flashcards.query.filter_by(id=deck_id).first()
    subject = flashcard_deck.subject
    subtopic = flashcard_deck.subtopic
    missed_flashcards = flashcard_deck.missed_flashcards
    # HACK Add the deck ID to the missed flashcards list
    # so that the JS script can use it to save the flashcards
    # back to the database after loading them.
    missed_flashcards.append(deck_id)
    correct_flashcards = flashcard_deck.correct_flashcards

    return render_template('flashcards.html', subject=subject,
                           subtopic=subtopic,
                           missed_flashcards=missed_flashcards,
                           correct_flashcards=correct_flashcards)


# This route prompts the user for a subject and subtopic before actually
# displaying the quiz.
@app.route("/quiz")
@login_required
def quiz():
    return render_template('topics.html', subjects=SUBJECT_SUBTOPIC_DICT,
                           subject_dictionary=SUBJECT_SUBTOPIC_DICT)


# This route displays the quiz based on the subject and subtopic selected
# by the user on the previous form.
@app.route("/quiz", methods=['POST'])
@login_required
def quiz_post():
    subject = request.form.get('subject_selection')
    subtopic = request.form.get('subtopic_selection')
    return render_template('quiz.html', title='Quiz', subject=subject,
                           subtopic=subtopic)


# Creates quiz questions based on the subject and subtopic provided in
# the url. The questions are returned in a JSON format to be used by
# the JS Script in templates/quiz.html.
@app.route("/generate_quiz", methods=['POST'])
def generate_quiz():
    data = request.json
    subject = data.get("subject")
    subtopic = data.get("subtopic")
    quiz_data = run_quiz(CLIENT, subject, subtopic)
    return jsonify(quiz_data)


# Saves the results of a quiz to the database from the JSON sent
# from quiz.html
@app.route("/save_quiz_result", methods=['POST'])
@login_required
def save_quiz_result():
    data = request.json

    num_correct = data.get("num_correct")

    result = QuizResult(
        time=None,
        subject=data.get("subject"),
        subtopic=data.get("subtopic"),
        num_correct=num_correct,
        user=current_user
    )
    db.session.add(result)
    db.session.commit()

    # Update the User's XP and XP Level
    # Possible RACE CONDITION here (non-trivial to resolve)
    current_user.xp = current_user.xp + SCORE_TO_XP[num_correct]
    current_user.xp_level = xp_level(current_user.xp)
    db.session.commit()

    return redirect(url_for('quiz_results'))


# This route prompts the user for a subject and subtopic before actually
# displaying the active recall page.
@app.route("/recall")
@login_required
def recall():
    return render_template('topics.html', subjects=SUBJECT_SUBTOPIC_DICT,
                           subject_dictionary=SUBJECT_SUBTOPIC_DICT)


# This route is used to display the flashcards page with the subject and
# subtopic selected by the user. The subject and subtopic are passed as
# parameters in the URL from the previous form submission.
@app.route("/recall", methods=['POST'])
@login_required
def recall_post():
    subject = request.form.get('subject_selection')
    subtopic = request.form.get('subtopic_selection')

    return render_template('recall.html', title='Active Recall',
                           subject=subject, subtopic=subtopic)


@app.route("/signin")
def signin():
    return render_template('signin.html', title='Sign In')


@app.route('/signin', methods=['POST'])
def signin_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the
    # hashed password in the database
    if not user or not check_password_hash(user.password, password):
        # if the user doesn't exist or password is wrong, reload the page
        flash('Please check your login details and try again.')
        return redirect(url_for('signin'))

    # if the above check passes, we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('home'))


@app.route("/signup")
def signup():
    return render_template('signin.html', title='Sign Up')


@app.route('/signup', methods=['POST'])
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # Make sure username is valid
    if len(username) < 2 or len(username) > 20:
        flash('Invalid Username! Please try again')
        return redirect(url_for('signup'))

    # Make sure passwords match
    if password != request.form.get('confirm_password'):
        flash('Passwords do not match! Please try again')
        return redirect(url_for('signup'))

    # if this returns a user, then the username already exists in database
    user = User.query.filter_by(username=username).first()

    # if a user is found, redirect back to signup page so user can try again
    if user:
        flash('Username already exists! Please try a different one')
        return redirect(url_for('signup'))

    # create a new user with the form data.
    # Hash the password so the plaintext version isn't saved.
    new_user = User(
        username=username,
        password=generate_password_hash(password, method='pbkdf2:sha256'),
        xp=0,
        xp_level=xp_level(0)
    )

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user, remember=remember)
    return redirect(url_for('home'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='LearnMateAI Profile')


# Show the user's past quiz history
@app.route('/quiz_results')
@login_required
def quiz_results():
    results = list(current_user.quiz_results)
    results.reverse()
    return render_template('quiz_results.html', title='Past Quiz Results',
                           results=results)


# Allow a user to review previous flashcard decks
@app.route('/saved_flashcards')
@login_required
def saved_flashcards():
    return render_template('saved_flashcards.html', title='Saved Flashcards')


@app.route('/leaderboard')
def leaderboard():
    leaders = User.query.order_by(User.xp.desc()).limit(10)
    return render_template('leaderboard.html', title='Global Leaderboard',
                           leaders=leaders)


# This route is used by pythonanywhere to update the server automatically
#  when a push is made to the GitHub repository.
@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/LearnMateAI/LearnMate')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
