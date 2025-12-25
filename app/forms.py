from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class LoginForm(FlaskForm):
    identifier = StringField('Username or Email', validators=[DataRequired(), Length(min=3, max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        from .models import User
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('Username already taken')

    def validate_email(self, email):
        from .models import User
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Email already registered')


class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=140)])
    description = TextAreaField('Short description', validators=[Length(max=500)])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()])
    steps = TextAreaField('Steps', validators=[DataRequired()])
    tags = StringField('Tags (comma separated)')
    image = FileField('Upload image')
    image_url = StringField('Or image URL')
    submit = SubmitField('Submit')
