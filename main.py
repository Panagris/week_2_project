from flask import Flask, render_template, url_for, flash, redirect, jsonify, \
    session, Blueprint, request
from flask_session import Session
from forms import RegistrationForm
from flask_sqlalchemy import SQLAlchemy
from flask_behind_proxy import FlaskBehindProxy
from flashcards import run_flashcards
import os
import git


db = SQLAlchemy()

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
proxied = FlaskBehindProxy(app)

#  TODO: Add a secret key to the app.config dictionary.
app.config['SECRET_KEY'] = '70dd3b360c7b766a43f2db955ad41043'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db.init_app(app)
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
def flashcards():
    return render_template('flashcards.html', title='Flashcards',
                           definition='Flashcards', signin=True)


@app.route("/get-cards")
def get_cards():
    # List of strings you want to send back to the client
        # Clear the session data related to flashcards
    session.pop('session_flashcards', None)    
    flashcards= run_flashcards("Math", "Algebra")
    session['session_flashcards'] = flashcards

    return jsonify(flashcards)


@app.route("/quiz")
def quiz():
    return render_template('quiz.html', title='Quiz')


@app.route("/signin")
def signin():
    return render_template('signin.html', title='Sign In', signin=True)


@app.route("/signup")
def signup():
    return render_template('signin.html', title='Sign Up', signin=False)


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
