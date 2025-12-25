from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=140)])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()])
    steps = TextAreaField('Steps', validators=[DataRequired()])
    tags = StringField('Tags (comma separated)')
    image = FileField('Image')
    submit = SubmitField('Submit')
