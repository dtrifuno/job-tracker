import graphene

from app.api.schema.auth import Query as AuthQuery, Mutation as AuthMutation
from app.api.schema.profile import Query as ProfileQuery, Mutation as ProfileMutation


class Query(AuthQuery, ProfileQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, ProfileMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
