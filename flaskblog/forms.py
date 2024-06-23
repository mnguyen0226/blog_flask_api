from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import BooleanField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import Email
from wtforms.validators import EqualTo
from flaskblog.models import User
from wtforms.validators import ValidationError
from flask_login import current_user


class RegistrationForm(FlaskForm):
    # Attributes
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    # On Form, make sure that there is no duplication. No need to call the function
    def validate_username(self, username):
        """Check if the username is in database"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "That username is taken. Please choose a different one."
            )

    # On Form, make sure that there is no duplication. No need to call the function
    def validate_email(self, email):
        """Check if the email is in database"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")


class LoginForm(FlaskForm):
    # Attributes
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])

    # Using a secured cookies to allow user to stay log-in
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    # Attributes
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Update")

    # On Form, make sure that there is no duplication. No need to call the function
    def validate_username(self, username):
        """Check if the username is in database"""
        # Only ping the database if the current username != the one in the database
        if current_user.username != username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "That username is taken. Please choose a different one."
                )

    # On Form, make sure that there is no duplication. No need to call the function
    def validate_email(self, email):
        """Check if the email is in database"""
        # Only ping the database if the current email != the one in the database
        if current_user.email != email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    "That email is taken. Please choose a different one."
                )
