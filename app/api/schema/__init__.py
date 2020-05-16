from functools import wraps

from flask import request
from flask_graphql_auth import get_jwt_identity
from flask_graphql_auth.decorators import _extract_header_token_value, verify_jwt_in_argument
import graphene
from graphql import GraphQLError
from graphql_relay import from_global_id

from app.api.models import User as UserModel, \
    Job as JobModel, \
    Event as EventModel, \
    Address as AddressModel, \
    Education as EducationModel, \
    Skill as SkillModel, \
    WorkExperience as WorkExperienceModel, \
    PersonalProject as PersonalProjectModel


def query_header_jwt_required(fn):
    """
    A decorator to protect a query resolver.
    Unlike the default Flask-GraphQL-Auth decorator, which returns an
    AuthInfoField on an authorization failure, this one raises a GraphQLError
    and thus does not require using union types.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = _extract_header_token_value(request.headers)
        try:
            verify_jwt_in_argument(token)
        except Exception as e:
            raise GraphQLError(f"Authorization failure: {str(e)}")

        return fn(*args, **kwargs)

    return wrapper


def mutation_header_jwt_required(fn):
    """
    A decorator to protect a mutation.
    Unlike the default Flask-GraphQL-Auth decorator, which returns an
    AuthInfoField on an authorization failure, this one raises a GraphQLError
    and thus does not require using union types.
    """

    @wraps(fn)
    def wrapper(cls, *args, **kwargs):
        token = _extract_header_token_value(request.headers)
        try:
            verify_jwt_in_argument(token)
        except Exception as e:
            raise GraphQLError(f"Authorization failure: {str(e)}")
        return fn(cls, *args, **kwargs)
    return wrapper


def get_user():
    username = get_jwt_identity()
    user = UserModel.query.filter_by(username=username).first()
    return user


def get_from_gid(gid):
    type_name, id = from_global_id(gid)
    type_to_model = {
        "JobType": JobModel,
        "EventType": EventModel,
        "AddressType": AddressModel,
        "EducationType": EducationModel,
        "SkillType": SkillModel,
        "WorkExperienceType": WorkExperienceModel,
        "PersonalProjectType": PersonalProjectModel
    }
    model = type_to_model.get(type_name, None)
    if model is None:
        raise GraphQLError(f"{type_name} is not a recognized GraphQL type.")

    item = model.query.get(id)
    user = get_user()
    if item.user != user:
        raise GraphQLError(f"{user} is not the owner of {item}.")
    return item


from app.api.schema.auth import Query as AuthQuery, Mutation as AuthMutation  # noqa
from app.api.schema.profile import Query as ProfileQuery, Mutation as ProfileMutation  # noqa
from app.api.schema.jobs import Query as JobsQuery, Mutation as JobsMutation  # noqa


class Query(AuthQuery, ProfileQuery, JobsQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, ProfileMutation, JobsMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
