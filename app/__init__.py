from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)

#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///storage.db"
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config.from_object("config")

db = SQLAlchemy(app)
migrate = Migrate(app,db)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

from app.models.tables import User, Post, Follow
from app.controllers import default

