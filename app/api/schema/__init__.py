import graphene
from flask_graphql_auth import get_jwt_identity

from app.api.models import User as UserModel


def get_user():
    username = get_jwt_identity()
    return UserModel.query.filter_by(username=get_jwt_identity()).first()



from app.api.schema.auth import Query as AuthQuery, Mutation as AuthMutation  # noqa
from app.api.schema.profile import Query as ProfileQuery, Mutation as ProfileMutation  # noqa


class Query(AuthQuery, ProfileQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, ProfileMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
