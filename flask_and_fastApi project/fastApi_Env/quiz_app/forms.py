# from blog import app

from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, validators, PasswordField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf.file import FileField, FileRequired, FileAllowed


# create form class 

class Registraion(FlaskForm):

    user_name = StringField('Username', validators=[DataRequired()])
    mobile_number = StringField('Mobile Number',  validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    # confirm_password = PasswordField('Confirm Password', validators=[DataRequired() , EqualTo('confirm_passowrd', message='Passwords must match')])
    
    submit  = SubmitField('Submit')

    
    def __repr__(self):
        return '<Username %r>' % self.user_name


class Login(FlaskForm):
    user_name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit  = SubmitField('Submit')


    