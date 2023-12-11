from flask import Flask
from config import Config
from dbInterface import DBInterface
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, login_user

app = Flask(__name__)

db = DBInterface()

bootstrap = Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)

app.config.from_object(Config)

from app import routes
