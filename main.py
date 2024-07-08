from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
import os

app = Flask(__name__)
proxied = FlaskBehindProxy(app)
#  TODO: Add a secret key to the app.config dictionary.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


# EXAMPLE FORMATS
@app.route("/")
def home():
    return render_template('home.html', subtitle='Home Page', text='This is the home page')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")