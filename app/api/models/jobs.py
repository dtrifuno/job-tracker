import datetime
import functools
import re
import string

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

import validators

from . import db


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
        if value.strip() == '':
            raise ValueError("Company is a required field.")
        return value

    @validates("position")
    def validate_position(self, key, value):
        if value.strip() == '':
            raise ValueError("Position is a required field.")
        return value

    @validates("location")
    def validate_location(self, key, value):
        if value.strip() == '':
            raise ValueError("Location is a required field.")
        return value


@functools.total_ordering
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    deadline = db.Column(db.String(10))
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

        for status in ("JobAdded", "Note", "ApplicationSubmitted",
                       "ScreeningScheduled", "ScreeningCompleted",
                       "AssessmentScheduled", "AssessmentCompleted",
                       "InterviewScheduled", "InterviewCompleted",
                       "Rejected",
                       "OfferMade", "OfferAccepted", "OfferRejected"):
            if self.event_type == status:
                return True
            elif other.event_type == status:
                return False
