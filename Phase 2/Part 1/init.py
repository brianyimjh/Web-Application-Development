from flask import Flask, render_template, redirect, url_for, request, jsonify
from datetime import datetime

from models import FitwellUser, FitwellLog
import json

def create_app():
    app = Flask(__name__)
    return app