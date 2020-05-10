import graphene
from flask_graphql_auth import get_jwt_identity

from app.api.models import User as UserModel


def get_user():
    username = get_jwt_identity()
    return UserModel.query.filter_by(username=get_jwt_identity()).first()

from app.api.schema.auth import Query as AuthQuery, Mutation as AuthMutation  # noqa
from app.api.schema.profile import Query as ProfileQuery, Mutation as ProfileMutation  # noqa
from app.api.schema.jobs import Query as JobsQuery, Mutation as JobsMutation  # noqa


class Query(AuthQuery, ProfileQuery, JobsQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, ProfileMutation, JobsMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
