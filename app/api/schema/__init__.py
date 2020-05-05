import graphene

from app.api.schema.auth import Query as AuthQuery
from app.api.schema.auth import Mutation as AuthMutation

schema = graphene.Schema(query=AuthQuery, mutation=AuthMutation)
