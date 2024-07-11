from flask import Flask, render_template, url_for, flash, redirect, Blueprint,\
    request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm
from flask_sqlalchemy import SQLAlchemy
from flask_behind_proxy import FlaskBehindProxy
from flask_login import UserMixin, LoginManager, login_user, login_required,\
    logout_user
from flask_session import Session
from flashcards import run_flashcards
import os
import git
import openai
from gpt_tutor import CLIENT, run_quiz


db = SQLAlchemy()


class User(UserMixin, db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
proxied = FlaskBehindProxy(app)

#  TODO: Add a secret key to the app.config dictionary.
app.config['SECRET_KEY'] = '70dd3b360c7b766a43f2db955ad41043'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tutor.db'

db.init_app(app)

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.login_view = "signin"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table,
    # use it in the query for the user
    return User.query.get(int(user_id))

Session(app)
# main = Blueprint('main', __name__)
# auth = Blueprint('auth', __name__)

# app.register_blueprint(auth)
# app.register_blueprint(main)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')


@app.route("/flashcards")
@login_required
def flashcards():
    return render_template('flashcards.html', title='Flashcards',
                           definition='Flashcards', signin=True)


@app.route("/get-cards")
def get_cards():
    # List of strings you want to send back to the client
    # Clear the session data related to flashcards
    session.pop('session_flashcards', None)
    flashcards = run_flashcards("Math", "Algebra")
    session['session_flashcards'] = flashcards

    return jsonify(flashcards)


@app.route("/quiz")
@login_required
def quiz():
    return render_template('quiz.html', title='Quiz')


@app.route("/generate_quiz", methods=['POST'])
def generate_quiz():
    data = request.json
    subject = data.get("subject", "History")
    subtopic = data.get("subtopic", "American Revolution")
    quiz_data = run_quiz(CLIENT, subject, subtopic)
    return jsonify(quiz_data)


@app.route("/signin")
def signin():
    return render_template('signin.html', title='Sign In')


@app.route('/signin', methods=['POST'])
def signin_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

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
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # if this returns a user, then the email already exists in database
    user = User.query.filter_by(email=email).first()

    # if a user is found, redirect back to signup page so user can try again
    if user:
        flash('Email address already exists')
        return redirect(url_for('signup'))

    # create a new user with the form data.
    # Hash the password so the plaintext version isn't saved.
    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password, method='pbkdf2:sha256')
    )

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('signin'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():  # checks if entries are valid
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))  # if so - send to home page
    return render_template('register.html', title='Register', form=form)


@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/LearnMateAI/LearnMate')
        repo.heads.deployment_testing.checkout()
        origin = repo.remotes.origin
        origin.pull('deployment_testing')
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
