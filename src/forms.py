from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email, Regexp, ValidationError, InputRequired


app = Flask(__name__)
app.secret_key = "your_secret_key"

# WTForms Class
class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Username is required."),
            Length(min=1, max=25, message="Username must be between 4 and 25 characters."),
        ],
        render_kw={"class": "form-control", "placeholder": "Enter your username"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(message="Password is required.")],
        render_kw={"class": "form-control", "placeholder": "Enter your password"},
    )
    submit = SubmitField("Login", render_kw={"class": "btn btn-primary"})

class VerifyCodeForm(FlaskForm):
    code = StringField(
        validators=[DataRequired(message="Verification code is required."), Length(min=4, max=6, message="Code must be between 4 and 6 characters.")],
        render_kw={"class": "form-control", "placeholder": "Enter verification code"}
    )
    submit = SubmitField("Verify code", render_kw={"class": "btn btn-primary"})


def validate_mobile_number(form, field):
    if not field.data.startswith('+'):
        raise ValidationError('Mobile number must start with a "+"')
    if len(field.data[1:]) < 10:  # This ensures the number is long enough (land code + number)
        raise ValidationError('Mobile number is too short, please include a valid land code.')


class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=1, max=20)],
        render_kw={"class": "form-control", "placeholder": "Enter username"}
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=3)],
        render_kw={"class": "form-control", "placeholder": "Enter password"}
    )
    email = EmailField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"class": "form-control", "placeholder": "Enter email"}
    )
    mobile_nr = StringField(
        "Mobile Number",
        validators=[DataRequired(), validate_mobile_number],
        render_kw={"class": "form-control", "placeholder": "Enter mobile number"}
    )
    submit = SubmitField("Register", render_kw={"class": "btn btn-primary"})

class ResetPasswordForm(FlaskForm):
    mail = StringField('Mail', validators=[InputRequired(), Email()])