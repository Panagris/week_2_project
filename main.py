from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
import os

app = Flask(__name__)
proxied = FlaskBehindProxy(app)
#  TODO: Add a secret key to the app.config dictionary.
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


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


@app.route("/signin")
def signin():
    return render_template('signin.html', title='Sign In')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
