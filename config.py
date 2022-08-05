import os
#import psycorg2
from local import *
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + db_username + ':' + db_password + '@' + db_host + '/' + db_name
    SQLALCHEMY_DATABASE_URI = 'postgresql://' + db_username + ':' + db_password + '@' + db_host + '/' + db_name
    #SQLALCHEMY_DATABASE_URI = "postgresql://postgres:kege@localhost:5432/kege"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 10