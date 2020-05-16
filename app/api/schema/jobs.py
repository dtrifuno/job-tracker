import re

from flask import render_template
from flask_graphql_auth import get_jwt_identity
import graphene
from graphql import GraphQLError
from graphql_relay import to_global_id
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from app.api.models import db
from app.api.models import Job as JobModel, Event as EventModel
from app.api.utils import extract_github_profile, extract_hostname, extract_linkedin_profile, to_month_year_string, group_skills
from . import get_user, get_from_gid, query_header_jwt_required, mutation_header_jwt_required


class EventType(SQLAlchemyObjectType):
    class Meta:
        model = EventModel
        interfaces = (relay.Node,)


class JobType(SQLAlchemyObjectType):
    class Meta:
        model = JobModel
        interfaces = (relay.Node,)

    events = graphene.List(EventType)


class CVType(graphene.ObjectType):
    address = graphene.ID()
    education = graphene.List(graphene.ID)
    skills = graphene.List(graphene.ID)
    work_history = graphene.List(graphene.ID)
    projects = graphene.List(graphene.ID)


def _extract_cv(job):
    result = CVType(
        education=[to_global_id("EducationType", school.id)
                   for school in job.education],
        skills=[to_global_id("SkillType", skill.id) for skill in job.skills],
        work_history=[to_global_id("WorkExperienceType", job.id)
                      for job in job.work_history],
        projects=[to_global_id("PersonalProjectType", project.id)
                  for project in job.projects]
    )
    if job.address:
        result.address = to_global_id("AddressType", job.address[0].id)
    return result


class Query(graphene.ObjectType):
    jobs = graphene.List(JobType)
    job = graphene.Field(JobType, args={"id": graphene.ID(required=True)})
    cv = graphene.Field(CVType, args={"id": graphene.ID(required=True)})
    cv_html = graphene.String(args={"id": graphene.ID(required=True)})

    @query_header_jwt_required
    def resolve_jobs(self, info):
        user = get_user()
        return user.jobs

    @query_header_jwt_required
    def resolve_job(self, info, id):
        job = get_from_gid(id)
        return job

    @query_header_jwt_required
    def resolve_cv(self, info, id):
        job = get_from_gid(id)
        return _extract_cv(job)

    @query_header_jwt_required
    def resolve_cv_html(self, info, id):
        user = get_user()
        job = get_from_gid(id)

        profile = user.profile
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

        if job.address:
            address = job.address[0]
            kwargs["address"] = str(address)

        kwargs["education"] = sorted(job.education, key=lambda x: x.date_from)
        kwargs["skills"] = group_skills(job.skills)
        kwargs["work_history"] = job.work_history
        kwargs["projects"] = job.projects

        kwargs["utils"] = {
            "to_month_year_string": to_month_year_string,
            "extract_hostname": extract_hostname
        }

        return render_template("cv.html", **kwargs)


class JobInput(graphene.InputObjectType):
    company = graphene.String()
    position = graphene.String()
    location = graphene.String()
    url = graphene.String()
    description = graphene.String()
    cover_letter = graphene.String()


class CreateJob(graphene.Mutation):
    class Arguments:
        date = graphene.String(required=True)
        job_data = JobInput(required=True)

    job = graphene.Field(JobType)

    @mutation_header_jwt_required
    def mutate(root, info, date, job_data):
        user = get_user()
        job = JobModel(user=user, **job_data)
        date_added = EventModel(
            date=date, event_type="JobAdded", user=user, job=job)
        db.session.add(job)
        db.session.add(date_added)
        db.session.commit()
        return CreateJob(job=job)


class DeleteJob(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @mutation_header_jwt_required
    def mutate(root, info, id):
        job = get_from_gid(id)
        db.session.delete(job)
        db.session.commit()
        return DeleteJob(ok=True)


class EditJob(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        job_data = JobInput(required=True)

    job = graphene.Field(JobType)

    @mutation_header_jwt_required
    def mutate(root, info, id, job_data):
        job = get_from_gid(id)
        job.update(job_data)
        db.session.commit()
        return EditJob(job=job)


class EventInput(graphene.InputObjectType):
    event_type = graphene.String()
    date = graphene.String()
    event_date = graphene.String()
    comment = graphene.String()


class CreateEvent(graphene.Mutation):
    class Arguments:
        job_id = graphene.ID(required=True)
        event_data = EventInput(required=True)

    event = graphene.Field(EventType)

    @mutation_header_jwt_required
    def mutate(root, info, job_id, event_data):
        if event_data.event_type == "JobAdded":
            raise GraphQLError("Events of this type cannot be created.")
        user = get_user()
        job = get_from_gid(job_id)
        event = EventModel(user=user, job=job, **event_data)
        db.session.add(event)
        db.session.commit()
        return CreateEvent(event=event)


class EditEvent(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        event_data = EventInput(required=True)

    event = graphene.Field(EventType)

    @mutation_header_jwt_required
    def mutate(root, info, id, event_data):
        if event_data.event_type == "JobAdded":
            raise GraphQLError("Events of this type cannot be edited.")
        event = get_from_gid(id)
        if event.event_type == "JobAdded":
            raise GraphQLError("Events of this type cannot be edited.")
        event.update(event_data)
        db.session.commit()
        return EditEvent(event=event)


class DeleteEvent(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @mutation_header_jwt_required
    def mutate(root, info, id):
        event = get_from_gid(id)
        if event.event_type == "JobAdded":
            raise GraphQLError("Events of this type cannot be deleted.")
        db.session.delete(event)
        db.session.commit()
        return DeleteJob(ok=True)


class SelectCVItems(graphene.Mutation):
    class Arguments:
        job_id = graphene.ID(required=True)
        add_ids = graphene.List(graphene.ID, required=True)
        remove_ids = graphene.List(graphene.ID, required=True)

    cv = graphene.Field(CVType)

    @mutation_header_jwt_required
    def mutate(root, info, job_id, add_ids, remove_ids):
        job = get_from_gid(job_id)

        for item_id in add_ids:
            item = get_from_gid(item_id)
            item.jobs.append(job)

        for item_id in remove_ids:
            item = get_from_gid(item_id)
            item.jobs.remove(job)

        db.session.commit()
        cv = _extract_cv(job)
        return SelectCVItems()


class Mutation(graphene.ObjectType):
    create_job = CreateJob.Field()
    edit_job = EditJob.Field()
    delete_job = DeleteJob.Field()
    create_event = CreateEvent.Field()
    edit_event = EditEvent.Field()
    delete_event = DeleteEvent.Field()
    select_cv_items = SelectCVItems.Field()
