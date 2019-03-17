from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, FormField, FieldList, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from bokchoi.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=5, max=30)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')



class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=5, max=30)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = StringField('Update Profile Picture url', validators=[Length(min=5, max=200)])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')



class ListForm(FlaskForm):
    ing = StringField('Ingredient')



class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=20)])
    description = StringField('Description', validators=[DataRequired(), Length(min=3, max=30)])
    ethnicity = SelectField('Ethnicity', choices=[('British', 'British'), ('French', 'French'), ('Medit', 'Medit'), ('Indian', 'Indian'), ('Middle East', 'Middle East'), ('Asian', 'Asian'), ('African', 'African'), ('Mexican', 'Mexican'), ('Other', 'Other')])
    vegan = BooleanField('Vegan')
    vegetarian = BooleanField('Vegetarian')
    nuts = BooleanField('Nuts')
    shellfish = BooleanField('Shellfish')
    meat = BooleanField('Meat')
    course = SelectField('Course', choices=[('Starter', 'Starter'), ('Main', 'Main'), ('Desert', 'Desert')])
    cook_time = IntegerField('Cooking Time', validators=[DataRequired()])
    ingredient = FieldList(StringField(ListForm), min_entries=6, max_entries=10)
    howto = TextAreaField('Howto', validators=[DataRequired(), Length(min=5, max=600)])
    picture = StringField('Image', validators=[DataRequired(), Length(min=5, max=200)], render_kw={"placeholder": "https://images.pexels.com/photos/958545/pexels-photo-958545.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500"})
    submit = SubmitField('Post')
