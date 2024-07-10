from flask import Flask, render_template, url_for, flash, redirect, Blueprint,request, jsonify
from forms import RegistrationForm
from flask_sqlalchemy import SQLAlchemy
from flask_behind_proxy import FlaskBehindProxy
import openai
from gpt_tutor import CLIENT, run_quiz 
import os





db = SQLAlchemy()

app = Flask(__name__)
proxied = FlaskBehindProxy(app)

#  TODO: Add a secret key to the app.config dictionary.
app.config['SECRET_KEY'] = '70dd3b360c7b766a43f2db955ad41043'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db.init_app(app)

# main = Blueprint('main', __name__)
# auth = Blueprint('auth', __name__)

# app.register_blueprint(auth)
# app.register_blueprint(main)


# EXAMPLE FORMATS
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')


@app.route("/flashcards")
def flashcards():
    return render_template('flashcards.html', title='Flashcards')


@app.route("/quiz")
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


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
