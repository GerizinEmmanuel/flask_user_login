from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.fields import EmailField 
from wtforms.validators import DataRequired, EqualTo, Length, Email

class LoginForm(FlaskForm):
    username=StringField("username",validators=[DataRequired()])
    password=PasswordField("password",validators=[DataRequired()])
    remember_me=BooleanField("remember_me")
 
class SignupForm(FlaskForm):
    username=StringField("username",validators=[DataRequired(message='Este campo é obrigatório.')])
    name=StringField("name",validators=[DataRequired(message='Este campo é obrigatório.')])
    email=EmailField("email",validators=[
        DataRequired(message='Este campo é obrigatório.'),
        Email(message='Introduz um e-mail válido.')])
    telefone=StringField("telefone",validators=[DataRequired(message='Este campo é obrigatório.')])
    password = PasswordField('new_password', validators=[
        Length(min=6,max=20, message='Digita uma palavra-passe que tenha de 6 a 20 caracteres.')
    ])
    confirm = PasswordField('confirm_password', validators=[EqualTo('password', message='As palavras-passe devem coincidir!'),]) 

class EditForm(FlaskForm):
    username=StringField("username",validators=[DataRequired(message='Este campo é obrigatório.')])
    name=StringField("name",validators=[DataRequired(message='Este campo é obrigatório.')])
    email=EmailField("email",validators=[
        DataRequired(message='Este campo é obrigatório.'),
        Email(message='Introduz um e-mail válido.')])
    telefone=StringField("telefone",validators=[DataRequired(message='Este campo é obrigatório.')])