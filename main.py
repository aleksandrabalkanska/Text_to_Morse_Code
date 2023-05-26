from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import InputRequired
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

morse_code_file = pd.read_csv('morse_code.csv')
morse_dict = {row.letter: row.code for (index, row) in morse_code_file.iterrows()}


class ConvertText(FlaskForm):

    text = TextAreaField('Text', validators=[InputRequired()])
    submit = SubmitField('Convert to Morse Code!')


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/converter", methods=["POST", "GET"])
def convert():
    form = ConvertText()
    output_text = None
    if form.validate_on_submit():
        user_input = list(form.text.data.lower().replace('\n', ' '))
        try:
            output = []
            for letter in user_input:
                if letter == ' ':
                    output.append('/')
                elif letter == '\n':
                    output.append('\n')
                else:
                    output.append(morse_dict[letter])
            output_text = '   '.join(output)
        except KeyError:
            flash('Invalid input!')
            return redirect(url_for('convert'))
    return render_template("converter.html", form=form, output=output_text)


if __name__ == '__main__':
    app.run(debug=True)