import datetime
import re

from sqlalchemy.orm import validates
from werkzeug.security import check_password_hash, generate_password_hash

from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_login = db.Column(db.DateTime)

    @validates('email')
    def validate_email(self, key, value):
        if self.query.filter_by(email=value).first():
            raise ValueError("Email is already registered.")
        elif not re.match("^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$", value):
            raise ValueError("Provided string is not a valid email address.")
        return value

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute.")

    @password.setter
    def password(self, password):
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters.")

        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'


class Profile(db.Model):
    # TODO: add user
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phone_number = db.Column(db.String(50))
    website_url = db.Column(db.String(50))
    github_url = db.Column(db.String(50))
    linkedin_url = db.Column(db.String(50))

    # TODO: Link these to User instead
    #addresses = db.relationship('Address', backref="profile", lazy=True)
    # education = db.relationship('Education', backref="profile", lazy=True)
    # skills = db.relationship('Skill', backref="profile", lazy=True)
    # work_history = db.relationship('WorkHistory', backref="profile", lazy=True)
    # personal_projects = db.relationship(
    #    'PersonalProject', backref = "profile", lazy = True)


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line_one = db.Column(db.String(50), nullable=False)
    line_two = db.Column(db.String(50))
    line_three = db.Column(db.String(50))


# class Education(db.Model):
#    pass
