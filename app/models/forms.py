from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField,MultipleFileField,SelectField,FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed, FileRequired

class LoginForm(Form):
    userName = StringField("userName",validators=[DataRequired()])
    password = PasswordField("password",validators=[DataRequired()])
    remember = BooleanField("remember")