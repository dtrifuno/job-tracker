import functools

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

from app.api import validators
from app.api.models import db


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(400), default="")
    description = db.Column(db.Text(15000), default="")
    cover_letter = db.Column(db.Text(10000), default="")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref("jobs", lazy=True))

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
