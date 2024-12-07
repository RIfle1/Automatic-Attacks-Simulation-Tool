from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)
app.secret_key = 'your_secret_key'
csrf = CSRFProtect(app)

class MyForm(FlaskForm):
    name = StringField('Name')
    submit = SubmitField('Submit')

class NoCSRFForm(FlaskForm):
    name = StringField('Name')
    submit = SubmitField('Submit')

@app.route('/')
def home():
    form = MyForm()
    return render_template('form.html', form=form)

@app.route('/submit', methods=['POST'])
def submit():
    form = MyForm()
    if form.validate_on_submit():
        name = form.name.data
        return f"Hello, {name}. Form submitted successfully!"
    return 'Form validation failed', 400

@app.route('/no_csrf')
def no_csrf():
    form = NoCSRFForm()
    return render_template('no_csrf_form.html', form=form)

@app.route('/submit_no_csrf', methods=['POST'])
def submit_no_csrf():
    form = NoCSRFForm()
    if form.validate_on_submit():
        name = form.name.data
        return f"Hello, {name}. Form submitted successfully without CSRF protection!"
    return 'Form validation failed', 400

if __name__ == '__main__':
    app.run(debug=True)