from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, InputRequired, Email, Length, EqualTo
from wtforms.fields.html5 import DateField
from app.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email')])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('LOGIN')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email')])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    password2 = PasswordField(
        'Repeat Password', validators=[InputRequired(), EqualTo('password')])
    firstname = StringField('First Name', validators=[InputRequired(), Length(min=2, max=20)])
    surname = StringField('Surname', validators=[InputRequired(), Length(min=2, max=20)])
    submit = SubmitField('REGISTER')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")



class WeddingForm(FlaskForm):
    partner = StringField('First Name', validators=[InputRequired(), Length(min=2, max=20)])
    wedding_date = DateField('DatePicker')
    submit = SubmitField('COMPLETE REGISTRATION')