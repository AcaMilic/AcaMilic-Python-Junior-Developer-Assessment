from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from app.models.models import Contact, User



class ContactForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=2, max=12)])
    phone = StringField('phone')
    company = StringField('company')
    email = StringField('email', validators=[DataRequired(), Email()])
    subject = StringField('subject')
    description = TextAreaField('description', validators=[DataRequired()])
    date = StringField('date')
    time = StringField('time')
    submit = SubmitField('Register')

    def validate_email(self, email):
        email = Contact.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is taken. Please choose a different one.')



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class UpdateAdminForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            username = User.query.filter_by(username=username.data).first()
            if username:
                raise ValidationError('That username is taken. Please choose a different one.')


    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That email is taken. Please choose a different one.')


    def validate_password(self, password):
        if password.data != current_user.password:
            password = User.query.filter_by(password=password.data).first()
            if password:
                raise ValidationError('That password is taken. Please choose a different one.')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')
