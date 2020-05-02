from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .profile import User  # noqa
