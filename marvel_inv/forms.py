from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email


class UserLoginForm(FlaskForm):
    #email, password, first_name, last_name
    email = StringField('Email', validators = [DataRequired(), Email()])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    password = PasswordField('Password', validators = [DataRequired()])
    submit_button = SubmitField()


class CharacterForm(FlaskForm):
    name = StringField('name')
    description = StringField('description')
    power = StringField('power')
    role = StringField('role')
    identity = StringField('identity')
    sidekick = StringField('sidekick')
    comic = IntegerField('comic')
    # date = StringField('date')
    submit_button = SubmitField()