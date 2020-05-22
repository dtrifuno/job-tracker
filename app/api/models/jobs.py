from datetime import date
import functools
import re

from flask import render_template, Markup
import markdown2
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

from app.api import validators
from app.api.models import db
from app.api.utils import extract_github_profile, extract_hostname, extract_linkedin_profile, to_month_year_string, group_skills


# TODO: Clean this up
address_job_relationship_table=db.Table('address_job_relationship_table', 
    db.Column('job_id', db.Integer,db.ForeignKey('job.id'), nullable=False),
    db.Column('address_id',db.Integer,db.ForeignKey('address.id'), nullable=False),
    db.PrimaryKeyConstraint('job_id', 'address_id') )

education_job_relationship_table=db.Table('education_job_relationship_table', 
    db.Column('job_id', db.Integer,db.ForeignKey('job.id'), nullable=False),
    db.Column('education_id',db.Integer,db.ForeignKey('education.id'), nullable=False),
    db.PrimaryKeyConstraint('job_id', 'education_id') )

skill_job_relationship_table=db.Table('skill_job_relationship_table', 
    db.Column('job_id', db.Integer,db.ForeignKey('job.id'), nullable=False),
    db.Column('skill_id',db.Integer,db.ForeignKey('skill.id'), nullable=False),
    db.PrimaryKeyConstraint('job_id', 'skill_id') )

work_experience_job_relationship_table=db.Table('work_experience_job_relationship_table', 
    db.Column('job_id', db.Integer,db.ForeignKey('job.id'), nullable=False),
    db.Column('work_experience_id',db.Integer,db.ForeignKey('work_experience.id'), nullable=False),
    db.PrimaryKeyConstraint('job_id', 'work_experience_id') )

personal_project_job_relationship_table=db.Table('personal_project_job_relationship_table', 
    db.Column('job_id', db.Integer,db.ForeignKey('job.id'), nullable=False),
    db.Column('personal_project_id',db.Integer,db.ForeignKey('personal_project.id'), nullable=False),
    db.PrimaryKeyConstraint('job_id', 'personal_project_id') )

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(400), default="")
    description = db.Column(db.Text(15000), default="")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref("jobs", lazy=True))

    # CV
    # TODO: Refactor into a separate model
    address = db.relationship('Address', secondary=address_job_relationship_table, backref="jobs")
    education = db.relationship('Education', secondary=education_job_relationship_table, backref="jobs")
    skills = db.relationship('Skill', secondary=skill_job_relationship_table, backref="jobs")
    projects = db.relationship('PersonalProject', secondary=personal_project_job_relationship_table, backref="jobs")
    work_history = db.relationship('WorkExperience', secondary=work_experience_job_relationship_table, backref="jobs")

    # Cover Letter
    # TODO: Refactor into a separate model
    recipient_name = db.Column(db.String(50))
    line_one = db.Column(db.String(50))
    line_two = db.Column(db.String(50))
    line_three = db.Column(db.String(50))
    city = db.Column(db.String(50))
    date = db.Column(db.String(10))
    subject_line = db.Column(db.String(50))
    opening_salutation = db.Column(db.String(100))
    cover_letter_body = db.Column(db.Text(10000), default="")
    closing_salutation = db.Column(db.String(100))


    @hybrid_property
    def date_created(self):
        return next(event for event in self.events if event.event_type == "JobAdded").date

    @hybrid_property
    def date_updated(self):
        return max(event.date for event in self.events)

    @hybrid_property
    def status(self):
        return max(self.events).event_type

    @validates("company")
    def validate_company(self, key, value):
        return validators.is_string(key, value, required=True)

    @validates("position")
    def validate_position(self, key, value):
        return validators.is_string(key, value, required=True)

    @validates("location")
    def validate_location(self, key, value):
        return validators.is_string(key, value, required=True)

    @validates("url")
    def validate_url(self, key, value):
        return validators.is_url(key, value)

    @hybrid_property
    def description_html(self):
        return markdown2.markdown(self.description)

    def header_html(self):
        profile = self.user.profile
        kwargs = {
            "first_name": profile.first_name,
            "last_name": profile.last_name
        }

        if profile.email:
            kwargs["email"] = {
                "url": f"mailto:{profile.email}",
                "email": profile.email
            }

        if profile.phone_number:
            number = profile.phone_number
            if re.match(r"^\d{10}$", number):
                kwargs["phone_number"] = {
                    "number": f"({number[:3]}) {number[3:6]}-{number[6:]}",
                    "url": f"tel:+1{number}"
                }
            else:
                kwargs["phone_number"] = {
                    "number": number
                }

        if profile.website_url:
            kwargs["website"] = {
                "url": profile.website_url,
                "hostname": extract_hostname(profile.website_url)
            }

        if profile.github_url:
            kwargs["github"] = {
                "url": profile.github_url,
                "profile": extract_github_profile(profile.github_url)
            }

        if profile.linkedin_url:
            kwargs["linkedin"] = {
                "url": profile.linkedin_url,
                "profile": extract_linkedin_profile(profile.linkedin_url)
            }

        if self.address:
            address = self.address[0]
            kwargs["address"] = str(address)


        kwargs["utils"] = {
            "to_month_year_string": to_month_year_string,
            "extract_hostname": extract_hostname
        }

        return render_template("header.html", **kwargs)

    @hybrid_property
    def cv_html(self):
        kwargs = {}
        kwargs["education"] = sorted(self.education, key=lambda x: x.date_from)
        kwargs["skills"] = group_skills(self.skills)
        kwargs["work_history"] = self.work_history
        kwargs["projects"] = self.projects

        kwargs["utils"] = {
            "to_month_year_string": to_month_year_string,
            "extract_hostname": extract_hostname
        }
        kwargs["header_html"] = Markup(self.header_html())

        return render_template("cv.html", **kwargs)

    @hybrid_property
    def cover_letter_html(self):
        kwargs = {}
        profile = self.user.profile
        kwargs["header_html"] = Markup(self.header_html())

        # Recipient
        kwargs["recipient"] = []
        if self.recipient_name:
            kwargs["recipient"].append(self.recipient_name)
        if self.line_one:
            kwargs["recipient"].append(self.line_one)
        if self.line_two:
            kwargs["recipient"].append(self.line_two)
        if self.line_three:
            kwargs["recipient"].append(self.line_three)

        # City and Date 
        date_str = None
        if self.date:
            date_str = date.fromisoformat(self.date).strftime("%B %d, %Y")
        if self.city and date_str:
            kwargs["city_and_date"] = ", ".join((self.city, date_str))
        elif self.city:
            kwargs["city_and_date"] = self.city
        elif self.date:
            kwargs["city_and_date"] = date_str

        if self.subject_line:
            kwargs["subject_line"] = self.subject_line

        if self.opening_salutation:
            kwargs["opening_salutation"] = self.opening_salutation

        if self.cover_letter_body:
            kwargs["cover_letter_body_html"] = Markup(markdown2.markdown(self.cover_letter_body))

        if self.closing_salutation:
            kwargs["closing_salutation"] = self.closing_salutation
            kwargs["name"] = " ".join((profile.first_name, profile.last_name))

        return render_template("cover_letter.html", **kwargs)




        



@functools.total_ordering
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    event_date = db.Column(db.String(10))
    comment = db.Column(db.String(200))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref("events", lazy=True))

    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    job = db.relationship('Job', backref=db.backref(
        "events", cascade="all,delete", lazy=True))

    def __eq__(self, other):
        return (self.date, self.event_type) == (other.date, other.event_type)

    def __lt__(self, other):
        if self.date != other.date:
            return self.date < other.date
        elif self.event_type == other.event_type:
            return False

        for status in validators.ordered_event_types:
            if self.event_type == status:
                return True
            elif other.event_type == status:
                return False

    @validates("event_type")
    def validates_event_type(self, key, value):
        return validators.is_event_type(key, value, required=True)

    @validates("date")
    def validates_date(self, key, value):
        return validators.is_date(key, value, required=True)

    @validates("event_date")
    def validates_event_date(self, key, value):
        return validators.is_date(key, value)

    @validates("comment")
    def validates_comment(self, key, value):
        return validators.is_string(key, value, remove_linebreaks=True)