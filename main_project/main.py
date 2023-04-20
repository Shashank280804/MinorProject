from flask import Flask, render_template, url_for, request, flash
from flask_wtf import FlaskForm
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

parking_system = Flask(__name__) # Application initialization.

login_manager = LoginManager()  # Login manager to add authentication functionality.
login_manager.init_app(parking_system)  # Initialize the login manager.

parking_system.secret_key = "yi5u9yh4gn"
csrf_token = "vaow457y34bvjr"

db = SQLAlchemy()  # Create database object.
parking_system.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///system.db"  # Set database path.
db.init_app(parking_system)  # Initialize the database.

# Forms
class Loginform(FlaskForm):
    """This class creates a login form."""
    email = EmailField('EMAIL-ID:', validators=[DataRequired()])
    password = PasswordField('PASSWORD:', validators=[DataRequired()])
    login = SubmitField('LOGIN')


#   Signup Form -
class Signup(FlaskForm):
    """This class creates a signup form."""
    name = StringField("NAME:", validators=[DataRequired(), Length(min=4, max=10)])
    email = EmailField('EMAIL-ID:', validators=[DataRequired()])
    password = PasswordField('SET PASSWORD:', validators=[DataRequired()])
    signup_button = SubmitField('SIGNUP')