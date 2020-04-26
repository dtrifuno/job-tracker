from flask import Blueprint

frontend = Blueprint('frontend', __name__)


@frontend.route('/')
def index():
    return '<h1>You are on the home page</h1>'
