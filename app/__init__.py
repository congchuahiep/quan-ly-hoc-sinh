import json
import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote

script_dir = os.path.dirname(__file__)
policy_path = os.path.join(script_dir, 'static/policy.json')

app = Flask(__name__)

app.secret_key = 'day la mot khoa cuc ky bi mat'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://admin:%s@localhost/quan_ly_hoc_sinh?charset=utf8mb4" % quote("Admin@123")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)
login_manager = LoginManager(app)

from app import routes
from app.auth import load_user