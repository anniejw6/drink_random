from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import basedir
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
bcrypt = Bcrypt()
lm.init_app(app)
bcrypt.init_app(app)

from app import views, models, forms

app.secret_key = 'gogogo'

