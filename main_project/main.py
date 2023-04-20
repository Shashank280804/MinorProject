from flask import Flask, render_template, url_for, request, flash, redirect
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_required
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from werkzeug import security as s

parking_system = Flask(__name__) # Application initialization.

login_manager = LoginManager()  # Login manager to add authentication functionality.
login_manager.init_app(parking_system)  # Initialize the login manager.

parking_system.secret_key = "yi5u9yh4gn"
csrf_token = "vaow457y34bvjr"

parking_system.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///system.db"  # Set database path.
db = SQLAlchemy(parking_system)  # Create database object.


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Database configuration
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), nullable=False)
    usr_email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class Vehicle(db.Model):
    __tablename__ ='vehicles'
    rfid = db.Column(db.Integer, primary_key=True)
    vehicle_name = db.Column(db.String(80), nullable=False)
    vehicle_type = db.Column(db.String(80), nullable=False)
    vehicle_plate = db.Column(db.String(80), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    vehicle_status = db.Column(db.Boolean, nullable=False)


# # Creating database
# with parking_system.app_context():
#     db.create_all()

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



with parking_system.app_context():
    vehicle_list = Vehicle.query.all()  # Get all vehicle information
    user_list = User.query.all()


parking_system.config['SECRET_KEY'] = csrf_token



# Function to hash passwords:
def hash_password(password):
    """This function hashes the user password. Converts password to SHA256 hash string with salt of length 8."""
    hashed_password = s.generate_password_hash(password=password, method='pbkdf2:sha256', salt_length=8)
    return hashed_password


# Function to check passwords:
def check_hash(user_hash, password):
    """This function checks if the password entered by the user is correct by comparing hashes."""
    check = s.check_password_hash(user_hash, password)
    return check


@parking_system.route("/")
def home():
    return render_template('header.html')


@parking_system.route("/login", methods=['GET', 'POST'])
def login():
    pass
    # form = Loginform()
    # if form.validate_on_submit():
    #     for user in user_list:
    #         if user.usr_email == form.email.data:
    #             if check_hash(user_hash=user.password, form.password.data):
    #                 login_user(user)
    #                 return redirect(url_for('home'))
    #             else:
    #                 flash('Invalid Password')


@parking_system.route("/signup", methods=['GET','POST'])
def signup():
    pass


@parking_system.route("/logout")
@login_required
def logout():
    pass


if __name__ == '__main__':
    # print(vehicle_list[0].vehicle_status)
    with parking_system.app_context():
        parking_system.run(debug=True)