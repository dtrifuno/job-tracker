import re


def extract_hostname(url):
    match = re.match(r"^https?://(.*)$", url)
    return match.group(1) if match else None


def extract_github_profile(url):
    match = re.match(
        r"^https?://(www.)?github.com/([a-zA-Z0-9\-]{1,39})$", url)
    return match.group(2) if match else None


def extract_linkedin_profile(url):
    match = re.match(
        r"^https?://(www.)?linkedin.com/in/([a-zA-Z0-9\-]{1,39})/$", url)
    return match.group(2) if match else None


def to_month_year_string(date_string):
    if not date_string:
        return "present"

    num_to_abbreviated_month = {
        "01": "Jan.",
        "02": "Feb.",
        "03": "Mar.",
        "04": "Apr.",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "Aug.",
        "09": "Sep.",
        "10": "Oct.",
        "11": "Nov.",
        "12": "Dec.",
    }

    year, month = re.match(r"^(\d{4})-([01]\d)$", date_string).groups()
    return f"{num_to_abbreviated_month[month]} {year}"


def group_skills(skills):
    categories = {skill.category for skill in skills}
    sorted_categories = sorted(list(categories))

    sorted_skills = {}
    for category in sorted_categories:
        sorted_skills[category] = sorted(
            [skill for skill in skills if skill.category == category], key=lambda x:x.skill)
    return {"sorted_categories": sorted_categories, "sorted_skills": sorted_skills}
