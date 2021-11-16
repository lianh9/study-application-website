from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField

from wtforms.validators import DataRequired

 
class LoginForm(FlaskForm):
    username = StringField('User', validators=[DataRequired()])
    password = PasswordField('Password')
    remember_me = BooleanField('Remember Me')

    submit = SubmitField('Sign in')

