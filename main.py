from flask import Flask, render_template, url_for, flash, redirect, jsonify, \
    session
from flask_session import Session
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
from flashcards import run_flashcards
import os

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
proxied = FlaskBehindProxy(app)
#  TODO: Add a secret key to the app.config dictionary.
app.config['SECRET_KEY'] = 'b1efe14252f08b51ef30a28b66860180'
# os.environ.get('SECRET_KEY')
Session(app)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')


@app.route("/flashcards")
def flashcards():

    if 'session_flashcards' not in session:
        session['session_flashcards'] = run_flashcards("Math", "Algebra")

    return render_template('flashcards.html', title='Flashcards',
                           definition='Flashcards', signin=True)


@app.route("/get-cards")
def get_cards():
    # List of strings you want to send back to the client
    flashcards = session.get('session_flashcards', {})
    return jsonify(flashcards)


@app.route("/quiz")
def quiz():
    return render_template('quiz.html', title='Quiz')


@app.route("/signin")
def signin():
    return render_template('signin.html', title='Sign In')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():  # checks if entries are valid
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))  # if so - send to home page
    return render_template('register.html', title='Register', form=form)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
