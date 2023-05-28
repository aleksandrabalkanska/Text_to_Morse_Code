from flask import Flask, render_template, flash
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
        user_input = form.text.data.lower()
        lines = user_input.split('\n')   # handles multiple line text
        try:
            output_text = ""
            for i, line in enumerate(lines):
                line_output = ""
                for letter in line:
                    if letter == ' ':
                        line_output += '/'    # / symbol for space in morse
                    else:
                        line_output += morse_dict.get(letter, '') + ' '
                output_text += line_output
                if i < len(lines) - 1:  # Add slash between lines if it's not the last line
                    output_text += '/ '
        except KeyError:
            flash('Invalid input!')
    return render_template("converter.html", form=form, output=output_text)


if __name__ == '__main__':
    app.run(debug=True)