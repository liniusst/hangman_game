from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField("username", [DataRequired()])
    email = StringField("email", [DataRequired()])
    password = PasswordField("password", [DataRequired()])
    confirm_password = PasswordField(
        "repeat password", [EqualTo("password", "Should match.")]
    )
    submit = SubmitField("sign in")


class LoginForm(FlaskForm):
    email = StringField("email", [DataRequired()])
    password = PasswordField("password", [DataRequired()])
    submit = SubmitField("log in")


class AccountUpdate(FlaskForm):
    username = StringField("username", [DataRequired()])
    email = StringField("email", [DataRequired()])
    submit = SubmitField("update")


class PasswordForm(FlaskForm):
    old_password = PasswordField("old password", [DataRequired()])
    new_password_first = PasswordField("new password", [DataRequired()])
    new_password_second = PasswordField(
        "new password",
        validators=[DataRequired(), EqualTo("new_password_first", "Should match.")],
    )
    submit = SubmitField("change")


class AddChar(FlaskForm):
    letter = StringField("letter", [DataRequired()])
    submit = SubmitField("submit")