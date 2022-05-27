from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, Length, input_required


class LoginForm(Form):
    print(input_required, ' 这里有变化，应选择其中一个！')
    email = StringField('Email', validators=[InputRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('keep me logged in')
    submit = SubmitField('Log In')



