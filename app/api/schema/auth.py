from graphql import GraphQLError
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from flask_graphql_auth import create_access_token, create_refresh_token

from app.api.models import db
from app.api.models import User as UserModel


class UserType(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    user = relay.Node.Field(UserType)


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        user = UserModel(username=username, password=password)
        token = create_access_token(username)
        db.session.add(user)
        db.session.commit()

        return CreateUser(user=user, token=token)


class Login(graphene.Mutation):
    class Arguments(object):
        username = graphene.String()
        password = graphene.String()

    token = graphene.String()

    @classmethod
    def mutate(cls, _, info, username, password):
        user = UserModel.query.filter_by(username=username).first()
        if (user and user.verify_password(password)):
            return Login(token=create_access_token(username))
        else:
            raise GraphQLError("Invalid credentials.")


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    login = Login.Field()
