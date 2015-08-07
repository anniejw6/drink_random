from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired
import random


class LoginForm(Form):
    """Form class for user login."""
    name = TextField('Username', validators=[DataRequired()])
   # remember_me = BooleanField('Remember me', default = False)