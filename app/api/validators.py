import re

import validators


def _print_key(key):
    return ' '.join(word.capitalize() for word in key.split('_'))


def _is_required(func):
    def wrapper_is_required(key, value, *args, required=False, **kwargs):
        if value is None or str(value).strip() == '':
            if required:
                raise ValueError(f"{_print_key(key)} is a required field.")
            else:
                return value
        return func(key, value, *args, **kwargs)
    return wrapper_is_required


@_is_required
def is_string(key, value, strip=False, dedupe_linebreaks=False, title_case=False, remove_linebreaks=False):
    if not isinstance(value, str):
        raise ValueError(
            f"Value {value} for field {_print_key(key)} is not a string.")
    result = value
    if strip:
        result = result.strip()
    if dedupe_linebreaks:
        result = re.sub(r"\n+", "\n", result)
    if title_case:
        result = result.title()
    if remove_linebreaks:
        result = result.replace('\n', '')
    return result


@_is_required
def is_year_month(key, value):
    if not re.match(r"^\d{4}-(0[1-9]|1[0-2])$", value):
        raise ValueError(f"{value} is not a valid yyyy-mm string.")
    return value


@_is_required
def is_date(key, value):
    if not re.match(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$", value):
        raise ValueError(f"{value} is not a valid yyyy-mm-dd string.")
    return value


@_is_required
def is_email(key, value):
    if not validators.email(value):
        raise ValueError(f"{value} is not a valid email address.")
    return value


@_is_required
def is_url(key, value):
    if not validators.url(value):
        raise ValueError(f"{value} is not a valid URL.")
    return value


@_is_required
def is_github_url(key, value):
    if not re.match(r"^https?://(www.)?github.com/[a-zA-Z0-9\-]{1,39}$", value):
        raise ValueError(f"{value} is not a valid Github URL.")
    return value


@_is_required
def is_linkedin_url(key, value):
    if not re.match(r"^https?://(www.)?linkedin.com/in/[a-zA-Z0-9\-]{1,39}/$", value):
        raise ValueError(f"{value} is not a valid LinkedIn URL.")
    return value


ordered_event_types = ["JobAdded", "Note", "ApplicationSubmitted",
                       "ScreeningScheduled", "ScreeningCompleted",
                       "AssessmentScheduled", "AssessmentCompleted",
                       "InterviewScheduled", "InterviewCompleted",
                       "Rejected", "OfferMade", "OfferAccepted", "OfferRejected"]


@_is_required
def is_event_type(key, value):
    if value not in ordered_event_types:
        raise ValueError(f"{value} is not a valid event type.")
    return value
