from flask_graphql_auth import get_jwt_identity
import graphene
from graphql import GraphQLError
from graphql_relay import to_global_id
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from app.api.models import db
from app.api.models import Job as JobModel, Event as EventModel
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


class CoverLetterType(graphene.ObjectType):
    recipient_name = graphene.String()
    line_one = graphene.String()
    line_two = graphene.String()
    line_three = graphene.String()
    city = graphene.String()
    date = graphene.String()
    subject_line = graphene.String()
    opening_salutation = graphene.String()
    cover_letter_body = graphene.String()
    closing_salutation = graphene.String()


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


def _extract_cover_letter(job):
    result = CoverLetterType(**{
        field: getattr(job, field, "") for field in ("recipient_name",
                                                 "line_one",
                                                 "line_two",
                                                 "line_three",
                                                 "city",
                                                 "date",
                                                 "subject_line",
                                                 "opening_salutation",
                                                 "cover_letter_body",
                                                 "closing_salutation")
    })
    return result


class Query(graphene.ObjectType):
    jobs = graphene.List(JobType)
    job = graphene.Field(JobType, args={"id": graphene.ID(required=True)})
    description_html = graphene.String(args={"id": graphene.ID(required=True)})
    cv = graphene.Field(CVType, args={"id": graphene.ID(required=True)})
    cv_html = graphene.String(args={"id": graphene.ID(required=True)})
    cover_letter = graphene.Field(
        CoverLetterType, args={"id": graphene.ID(required=True)})
    cover_letter_html = graphene.String(
        args={"id": graphene.ID(required=True)})

    @query_header_jwt_required
    def resolve_jobs(self, info):
        user = get_user()
        return user.jobs

    @query_header_jwt_required
    def resolve_job(self, info, id):
        job = get_from_gid(id)
        return job

    @query_header_jwt_required
    def resolve_description_html(self, info, id):
        job = get_from_gid(id)
        return job.description_html

    @query_header_jwt_required
    def resolve_cv(self, info, id):
        job = get_from_gid(id)
        return _extract_cv(job)

    @query_header_jwt_required
    def resolve_cv_html(self, info, id):
        job = get_from_gid(id)
        return job.cv_html

    @query_header_jwt_required
    def resolve_cover_letter(self, info, id):
        job = get_from_gid(id)
        return _extract_cover_letter(job)

    @query_header_jwt_required
    def resolve_cover_letter_html(self, info, id):
        job = get_from_gid(id)
        return job.cover_letter_html


class JobInput(graphene.InputObjectType):
    company = graphene.String()
    position = graphene.String()
    location = graphene.String()
    url = graphene.String()
    description = graphene.String()


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


class UpdateCV(graphene.Mutation):
    class Arguments:
        job_id = graphene.ID(required=True)
        add_ids = graphene.List(graphene.ID, required=True)
        remove_ids = graphene.List(graphene.ID, required=True)

    cv = graphene.Field(CVType)
    cv_html = graphene.String()

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
        return UpdateCV(cv=cv, cv_html=job.cv_html)


class CoverLetterInput(graphene.InputObjectType):
    recipient_name = graphene.String()
    line_one = graphene.String()
    line_two = graphene.String()
    line_three = graphene.String()
    city = graphene.String()
    date = graphene.String()
    subject_line = graphene.String()
    opening_salutation = graphene.String()
    cover_letter_body = graphene.String()
    closing_salutation = graphene.String()


class UpdateCoverLetter(graphene.Mutation):
    class Arguments:
        job_id = graphene.ID(required=True)
        cover_letter_data = CoverLetterInput(required=True)

    cover_letter = graphene.Field(CoverLetterType)
    cover_letter_html = graphene.String()

    @mutation_header_jwt_required
    def mutate(root, info, job_id, cover_letter_data):
        job = get_from_gid(job_id)
        job.update(cover_letter_data)
        db.session.commit()
        return UpdateCoverLetter(cover_letter=_extract_cover_letter(job), cover_letter_html=job.cover_letter_html)


class Mutation(graphene.ObjectType):
    create_job = CreateJob.Field()
    edit_job = EditJob.Field()
    delete_job = DeleteJob.Field()
    create_event = CreateEvent.Field()
    edit_event = EditEvent.Field()
    delete_event = DeleteEvent.Field()
    update_cv = UpdateCV.Field()
    update_cover_letter = UpdateCoverLetter.Field()
