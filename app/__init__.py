from flask import Flask
from flask_moment import Moment
from config import Config


app = Flask(__name__, static_folder="static")
app.config.from_object(Config)
moment = Moment(app)

from app import routes