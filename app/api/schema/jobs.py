from graphql import GraphQLError
from graphql_relay import from_global_id

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from flask_graphql_auth import get_jwt_identity, query_header_jwt_required, mutation_header_jwt_required

from . import get_user

from app.api.models import db
from app.api.models import Job as JobModel, \
    Event as EventModel


def get_from_gid(gid):
    type_name, id = from_global_id(gid)
    type_to_model = {
        "JobType": JobModel,
        "EventType": EventModel
    }
    print(type_name, id)
    model = type_to_model.get(type_name, None)
    if model is None:
        raise GraphQLError(f"{type_name} is not a recognized GraphQL type.")

    item = model.query.get(id)
    user = get_user()
    if item.user != user:
        raise GraphQLError(f"{user} is not the owner of {item}.")
    return item


class JobType(SQLAlchemyObjectType):
    class Meta:
        model = JobModel
        interfaces = (relay.Node,)


class EventType(SQLAlchemyObjectType):
    class Meta:
        model = EventModel
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    jobs = graphene.List(JobType)
    job = graphene.Field(JobType, args={"id": graphene.ID(required=True)})

    @query_header_jwt_required
    def resolve_jobs(self, info):
        user = get_user()
        return user.jobs

    @query_header_jwt_required
    def resolve_job(self, info, id):
        job = get_from_gid(id)
        return job


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
        date_added = EventModel(date=date, event_type="JobAdded", user=user, job=job)
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



class Mutation(graphene.ObjectType):
    create_job = CreateJob.Field()
    delete_job = DeleteJob.Field()
