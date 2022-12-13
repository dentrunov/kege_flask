from flask import Blueprint
from flask_simple_captcha import CAPTCHA

bp = Blueprint('reg', __name__)


from app.reg import forms, routes