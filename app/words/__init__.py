from flask import Blueprint

words = Blueprint("words", __name__)

from . import views