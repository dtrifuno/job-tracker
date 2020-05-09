import datetime
import re
import string

from sqlalchemy.orm import validates
import validators
from werkzeug.security import check_password_hash, generate_password_hash

from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    @validates('username')
    def validate_username(self, key, value):
        for whitespace in string.whitespace:
            if whitespace in value:
                raise ValueError("Username cannot contain whitespace.")
        if not 5 < len(value) < 20:
            raise ValueError(
                "Username must be between 6 and 20 characters in length.")
        if self.query.filter_by(username=value).first():
            raise ValueError("Username already token.")
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
        return f'<User {self.username}>'


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phone_number = db.Column(db.String(50))
    website_url = db.Column(db.String(50))
    github_url = db.Column(db.String(50))
    linkedin_url = db.Column(db.String(50))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref(
        "profile", uselist=False, lazy=True))

    @validates('email')
    def validate_email(self, key, value):
        if value.strip() == '':
            return ''
        elif not validators.email(value):
            raise ValueError(f"{value} is not a valid email address.")
        return value

    @validates('website_url')
    def validate_website_url(self, key, value):
        if value.strip() == '':
            return ''
        elif not validators.url(value):
            raise ValueError(f"{value} is not a valid URL.")
        return value

    @validates('github_url')
    def validate_github_url(self, key, value):
        if value.strip() == '':
            return ''
        elif not re.match(r"^https?://(www.)?github.com/[a-zA-Z0-9\-]{1,39}$", value):
            raise ValueError(f"{value} is not a valid Github URL.")
        return value

    @validates('linkedin_url')
    def validate_linkedin_url(self, key, value):
        if value.strip() == '':
            return ''
        elif not re.match(r"^https?://(www.)?linkedin.com/in/[a-zA-Z0-9\-]{1,39}/$", value):
            raise ValueError(f"{value} is not a valid LinkedIn URL.")
        return value


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line_one = db.Column(db.String(50), nullable=False)
    line_two = db.Column(db.String(50))
    line_three = db.Column(db.String(50))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref("addresses", lazy=True))

    @validates("line_one")
    def validate_line_one(self, key, value):
        if value.strip() == '':
            raise ValueError("Line One is a required field.")
        return value


def is_year_month(value):
    return bool(re.match(r"^\d{4}-\d{2}$", value))


class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50))
    degree_and_field = db.Column(db.String(50))
    date_from = db.Column(db.String(7), nullable=False)
    date_to = db.Column(db.String(7))
    gpa = db.Column(db.String(20))
    description = db.Column(db.Text(1000))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref("education", lazy=True))

    @validates("school")
    def validate_school(self, key, value):
        if value.strip() == '':
            raise ValueError("School is a required field.")
        return value

    @validates("date_from")
    def validate_date_from(self, key, value):
        if value.strip() == '':
            raise ValueError("Date From is a required field.")
        elif not is_year_month(value):
            raise ValueError(f"{value} is not a valid yyyy-mm string.")
        return value

    @validates("date_to")
    def validate_date_to(self, key, value):
        if value.strip() and not is_year_month(value):
            raise ValueError(f"{value} is not a valid yyyy-mm string.")
        return value

    @validates("description")
    def validate_description(self, key, value):
        return re.sub(r"\n+", "\n", value.strip())


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill = db.Column(db.String(50))
    category = db.Column(db.String(50))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('skills', lazy=True))

    @validates("skill")
    def validate_skill(self, key, value):
        if value.strip() == '':
            raise ValueError("Skill is a required field.")
        return value


class WorkExperience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50))
    date_from = db.Column(db.String(7), nullable=False)
    date_to = db.Column(db.String(7))
    description = db.Column(db.Text(1000))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(
        'User', backref=db.backref('work_history', lazy=True))

    @validates("company")
    def validate_company(self, key, value):
        if value.strip() == '':
            raise ValueError("Company is a required field.")
        return value

    @validates("position")
    def validate_position(self, key, value):
        if value.strip() == '':
            raise ValueError("Position is a required field.")
        return value

    @validates("date_from")
    def validate_date_from(self, key, value):
        if value.strip() == '':
            raise ValueError("Date From is a required field.")
        elif not is_year_month(value):
            raise ValueError(f"{value} is not a valid yyyy-mm string.")
        return value

    @validates("date_to")
    def validate_date_to(self, key, value):
        if value.strip() and not is_year_month(value):
            raise ValueError(f"{value} is not a valid yyyy-mm string.")
        return value

    @validates("description")
    def validate_description(self, key, value):
        return re.sub(r"\n+", "\n", value.strip())


class PersonalProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('personal_projects', lazy=True))

    @validates("project_name")
    def validate_project_name(self, key, value):
        if value.strip() == '':
            raise ValueError("Project Name is a required field.")
        return value

    @validates('url')
    def validate_url(self, key, value):
        if value.strip() == '':
            return ''
        elif not validators.url(value):
            raise ValueError(f"{value} is not a valid URL.")
        return value

    @validates("description")
    def validate_description(self, key, value):
        return re.sub(r"\n+", "\n", value.strip())