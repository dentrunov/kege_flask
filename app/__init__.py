from flask import Flask
from flask_moment import Moment
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, static_folder="static")
app.config.from_object(Config)
moment = Moment(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes