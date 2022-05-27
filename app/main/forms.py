from flask_wtf import Form
from wtforms import SubmitField, TextAreaField
from wtforms.validators import InputRequired


class PostForm(Form):
    body = TextAreaField("What's on your mind?", validators=[InputRequired()])
    submit = SubmitField('Submit')
