from flask_wtf import Form
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import InputRequired, data_required


class PostForm(Form):
    # name = StringField('what is you name', validators=[InputRequired()])
    password = TextAreaField('password')
    body = TextAreaField("What's on your mind?", validators=[InputRequired()])
    submit = SubmitField('Submit')
