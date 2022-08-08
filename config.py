import os
#import psycorg2
from local import *
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + db_username + ':' + db_password + '@' + db_host + '/' + db_name
    SQLALCHEMY_DATABASE_URI = 'postgresql://' + db_username + ':' + db_password + '@' + db_host + '/' + db_name
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 10
    #перенести в локал
    MAIL_SERVER = mail_server
    MAIL_PORT = mail_port
    MAIL_USE_TLS = mail_use_tls
    MAIL_USERNAME = mail_username
    MAIL_DEFAULT_SENDER = mail_default_sender
    MAIL_PASSWORD = mail_password
    MAIL_USE_SSL = mail_use_ssl