# Imports
from flask import Flask, render_template, url_for, request, flash, redirect
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from werkzeug import security as s


parking_system = Flask(__name__) # Application initialization.


login_manager = LoginManager()  # Login manager to add authentication functionality.
login_manager.init_app(parking_system)  # Initialize the login manager.


# Keys:
parking_system.secret_key = "yi5u9yh4gn"
csrf_token = "vaow457y34bvjr"


parking_system.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///system.db"  # Set database path.
db = SQLAlchemy(parking_system)  # Create database object.


# User loader.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Database configuration
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), nullable=False)
    usr_email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    flat_no = db.Column(db.Integer(), nullable=False, unique=True)
    aadhar_no = db.Column(db.Integer(), nullable=False, unique=True)


class Vehicle(db.Model):
    __tablename__ ='vehicles'
    rfid = db.Column(db.Integer, primary_key=True)
    vehicle_name = db.Column(db.String(80), nullable=False)
    vehicle_type = db.Column(db.String(80), nullable=False)
    vehicle_plate = db.Column(db.String(80), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    vehicle_status = db.Column(db.Boolean, nullable=False)
    v_time = db.Column(db.DateTime, nullable=False)


# Creating database
with parking_system.app_context():
    db.create_all()

# Forms
## Login Form
class Loginform(FlaskForm):
    """This class creates a login form."""
    email = EmailField('EMAIL-ID:', validators=[DataRequired()])
    password = PasswordField('PASSWORD:', validators=[DataRequired()])
    login = SubmitField('LOGIN')


## Signup Form -
class Signup(FlaskForm):
    """This class creates a signup form."""
    name = StringField("NAME:", validators=[DataRequired(), Length(min=4, max=10)])
    email = EmailField('EMAIL-ID:', validators=[DataRequired()])
    password = PasswordField('SET PASSWORD:', validators=[DataRequired()])
    flat_no = StringField('FLAT-NO:', validators=[DataRequired()])
    aadhar_no = StringField('AADHAR CARD-NO:', validators=[DataRequired()])
    signup = SubmitField('SIGNUP')


## Vehicle Form - 
class VehicleForm(FlaskForm):
    """This class creates a vehicle form"""
    vehicle_name = StringField("VEHICLE NAME:", validators=[DataRequired(), Length(min=4, max=10)])
    vehicle_type = StringField("VEHICLE TYPE:", validators=[DataRequired(), Length(min=4, max=10)])
    vehicle_plate = StringField("VEHICLE PLATE:", validators=[DataRequired(), Length(min=4, max=10)])
    add_veh = SubmitField('Add Vehicle')


## Profile Form -
class ProfileForm(FlaskForm):
    """This class represents profile form."""
    name = StringField("NAME:", validators=[DataRequired(), Length(min=4, max=10)])
    email = EmailField('EMAIL-ID:', validators=[DataRequired()])
    flat_no = StringField('Flat Number:', validators=[DataRequired()])
    aadhar_no = StringField('Aadhar Card Number:', validators=[DataRequired()])
    save_prof = StringField('Save Profile')

    

# Application context:
with parking_system.app_context():
    vehicle_list = Vehicle.query.all()  # Get all vehicle information from table.
    user_list = User.query.all()  # Get all user information from table.


# Storing csrf token in application.
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


# Routes:

@parking_system.route("/")
def home():
    return render_template('index.html', user_logged_in=current_user.is_authenticated, v_list=vehicle_list)


@parking_system.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user_logged_in=current_user.is_authenticated, u_list=user_list)


@parking_system.route("/vehicles")
@login_required
def vehicles():
    return render_template("vehicles.html", user_logged_in=current_user.is_authenticated, v_list=vehicle_list)

@parking_system.route("/login", methods=['GET', 'POST'])
def login():
    form = Loginform()
    val = True
    if form.validate_on_submit():
        for user in user_list:
            if user.usr_email == form.email.data and check_hash(user_hash=user.password, password=form.password.data):
                    val = True
                    login_user(user)
                    return redirect(url_for('home', user_logged_in=current_user.is_authenticated))
            else:
                val = False
        if val == False:
            flash('Invalid Email-ID or password')
    else:
        print("Not validated")

    return render_template("login.html", form=form)


@parking_system.route("/signup", methods=['GET','POST'])
def signup():
    form = Signup()
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = hash_password(password=form.password.data)
            new_user = User(user_name=form.name.data, usr_email=form.email.data, password=hashed_password, flat_no=form.flat_no.data, aadhar_no=form.aadhar_no.data)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('home', form = form, user_logged_in=current_user.is_authenticated))
        else:
            print("Not validated")
            print(form.aadhar_no.data)
    return render_template('signup.html', form=form, user_logged_in=current_user.is_authenticated)


@parking_system.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    # print(vehicle_list[0].vehicle_status)
    with parking_system.app_context():
        parking_system.run(debug=True)

# TO DO:
## Add vehicle form
## Edit profile form
## nav link - active link js code
## Connect arduino to database
## Remove 'profile' title from web page
## Design analytics page.