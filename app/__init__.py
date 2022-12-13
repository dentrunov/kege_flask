from flask import Flask
from flask_moment import Moment
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_simple_captcha import CAPTCHA
#import psycorg2
#import pymysql
#pymysql.install_as_MySQLdb()

app = Flask(__name__, static_folder="static")
app.config.from_object(Config)
moment = Moment(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
mail = Mail(app)
login.login_view = 'login'

CAPTCHA = CAPTCHA(config=Config.CAPTCHA_CONFIG)
app = CAPTCHA.init_app(app)


from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)
from app.reg import bp as reg_bp
app.register_blueprint(reg_bp, url_prefix='/reg')



from app import routes, models, forms, email

