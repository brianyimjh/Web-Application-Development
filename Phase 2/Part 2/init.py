from flask import Flask, render_template, redirect, url_for, request, jsonify, flash
from datetime import datetime

from models import FitwellUser, FitwellLog
import json

from flask_login import logout_user, login_required, current_user
from auth import Auth

def create_app():
    app = Flask(__name__)

    # Configure for your web application (1) Secret key
    app.config['SECRET_KEY'] = 'B14BB29DCAB6B72F1E34DC6B5BFE8'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    Auth.load(app)
       
    return app