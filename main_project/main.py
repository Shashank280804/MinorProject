from flask import Flask, render_template, url_for, request, flash
from flask_wtf import FlaskForm
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

parking_system = Flask(__name__) # Application initialization.

login_manager = LoginManager()  # Login manager to add authentication functionality.

parking_system.config['SQL_DB_URL'] = url_for("sqlite://system.db")

login_manager.init_app(parking_system)
