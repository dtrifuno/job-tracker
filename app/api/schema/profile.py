from graphql import GraphQLError
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from flask_graphql_auth import get_jwt_identity, query_header_jwt_required, mutation_header_jwt_required

from app.api.models import db
from app.api.models import User as UserModel, Profile as ProfileModel


class ProfileType(SQLAlchemyObjectType):
    class Meta:
        model = ProfileModel
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    profile = graphene.Field(ProfileType)

    @query_header_jwt_required
    def resolve_profile(self, info):
        username = get_jwt_identity()
        print(username)
        user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        return user.profile


class EditBiographicalData(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        phone_number = graphene.String()
        website_url = graphene.String()
        github_url = graphene.String()
        linkedin_url = graphene.String()

    profile = graphene.Field(ProfileType)

    @mutation_header_jwt_required
    def mutate(root, info, first_name, last_name, email, phone_number, website_url, github_url, linkedin_url):
        username = get_jwt_identity()
        user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        profile = user.profile
        profile.first_name = first_name
        profile.last_name = last_name
        profile.email = email
        profile.phone_number = phone_number
        profile.website_url = website_url
        profile.github_url = github_url
        profile.linkedin_url = linkedin_url
        db.session.add(profile)
        db.session.commit()

        return EditBiographicalData(profile=profile)


class Mutation(graphene.ObjectType):
    edit_biographical_data = EditBiographicalData.Field()
