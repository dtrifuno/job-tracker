from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # noqa

from .profile import User, Profile
