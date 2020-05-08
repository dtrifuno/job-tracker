from graphql import GraphQLError
from graphql_relay import from_global_id

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from flask_graphql_auth import get_jwt_identity, query_header_jwt_required, mutation_header_jwt_required

from app.api.models import db
from app.api.models import User as UserModel, \
    Profile as ProfileModel, \
    Address as AddressModel, \
    Education as EducationModel, \
    WorkExperience as WorkExperienceModel

# TODO: Refactor validated access


class ProfileType(SQLAlchemyObjectType):
    class Meta:
        model = ProfileModel
        interfaces = (relay.Node,)

class AddressType(SQLAlchemyObjectType):
    class Meta:
        model = AddressModel
        interfaces = (relay.Node,)

class EducationType(SQLAlchemyObjectType):
    class Meta:
        model = EducationModel
        interfaces = (relay.Node,)


class WorkExperienceType(SQLAlchemyObjectType):
    class Meta:
        model = WorkExperienceModel
        interfaces = (relay.Node,)




class Query(graphene.ObjectType):
    profile = graphene.Field(ProfileType)
    addresses = graphene.List(AddressType)
    education = graphene.List(EducationType)

    @query_header_jwt_required
    def resolve_profile(self, info):
        username = get_jwt_identity()
        user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        return user.profile

    @query_header_jwt_required
    def resolve_addresses(self, info):
        username = get_jwt_identity()
        user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        return user.addresses

    @query_header_jwt_required
    def resolve_education(self, info):
        username = get_jwt_identity()
        user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        return user.education


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
    def mutate(root, info, **kwargs):
        username = get_jwt_identity()
        user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        profile = ProfileModel.query.filter_by(user=user).first()
        profile.update(kwargs)
        db.session.commit()

        return EditBiographicalData(profile=profile)


class AddressInput(graphene.InputObjectType):
    line_one = graphene.String()
    line_two = graphene.String()
    line_three = graphene.String()


class CreateAddress(graphene.Mutation):
    class Arguments:
        address_data = AddressInput(required=True)

    address = graphene.Field(AddressType)

    @mutation_header_jwt_required
    def mutate(root, info, address_data):
        username = get_jwt_identity()
        user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        address = AddressModel(user=user, **address_data)
        db.session.add(address)
        db.session.commit()

        return CreateAddress(address=address)


class EditAddress(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        address_data = AddressInput(required=True)

    address = graphene.Field(AddressType)

    @mutation_header_jwt_required
    def mutate(root, info, id, address_data):
        username = get_jwt_identity()
        user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        db_id = from_global_id(id)[1]
        address = AddressModel.query.get(db_id)
        if address.user != user:
            pass
        address.update(address_data)
        db.session.commit()

        return EditAddress(address=address)


class DeleteAddress(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    ok = graphene.Boolean()

    def mutate(root, info, id):
        username = get_jwt_identity()
        user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        db_id = from_global_id(id)[1]
        address = AddressModel.query.get(db_id)
        if address.user != user:
            pass
        db.session.delete(address)
        db.session.commit()

        return DeleteAddress(ok=True)


class EducationExperienceInput(graphene.InputObjectType):
    school = graphene.String()
    location = graphene.String()
    degree_and_field = graphene.String()
    gpa = graphene.String()
    date_from = graphene.NonNull(graphene.String)
    date_to = graphene.String()
    description = graphene.String()


class CreateEducationExperience(graphene.Mutation):
    class Arguments:
        education_experience_data = EducationExperienceInput(required=True)

    education_experience = graphene.Field(EducationType)

    @mutation_header_jwt_required
    def mutate(root, info, education_experience_data):
        username = get_jwt_identity()
        user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        education = EducationModel(user=user, **education_experience_data)
        db.session.add(education)
        db.session.commit()

        return CreateEducationExperience(education_experience=education)


class EditEducationExperience(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        education_experience_data = EducationExperienceInput(required=True)

    education_experience = graphene.Field(EducationType)

    @mutation_header_jwt_required
    def mutate(root, info, id, education_experience_data):
        username = get_jwt_identity()
        user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        db_id = from_global_id(id)[1]
        education = EducationModel.query.get(db_id)
        if education.user != user:
            pass
        education.update(education_experience_data)
        db.session.commit()

        return EditEducationExperience(education_experience=education)


class DeleteEducationExperience(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    ok = graphene.Boolean()

    def mutate(root, info, id):
        username = get_jwt_identity()
        user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        db_id = from_global_id(id)[1]
        education = EducationModel.query.get(db_id)
        if education.user != user:
            pass
        db.session.delete(education)
        db.session.commit()

        return DeleteEducationExperience(ok=True)









class WorkExperienceInput(graphene.InputObjectType):
    school = graphene.String()
    location = graphene.String()
    degree_and_field = graphene.String()
    gpa = graphene.String()
    date_from = graphene.NonNull(graphene.String)
    date_to = graphene.String()
    description = graphene.String()


class CreateWorkExperience(graphene.Mutation):
    class Arguments:
        work_experience_data = WorkExperienceInput(required=True)

    work_experience = graphene.Field(WorkExperienceType)

    @mutation_header_jwt_required
    def mutate(root, info, work_experience_data):
        username = get_jwt_identity()
        user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        work_experience = WorkExperienceModel(user=user, **work_experience_data)
        db.session.add(work_experience)
        db.session.commit()

        return CreateWorkExperience(work_experience=work_experience)


class EditWorkExperience(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        work_experience_data = WorkExperienceInput(required=True)

    work_experience = graphene.Field(WorkExperienceType)

    @mutation_header_jwt_required
    def mutate(root, info, id, education_experience_data):
        username = get_jwt_identity()
        user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        db_id = from_global_id(id)[1]
        education = EducationModel.query.get(db_id)
        if education.user != user:
            pass
        education.update(education_experience_data)
        db.session.commit()

        return EditEducationExperience(education_experience=education)


class DeleteEducationExperience(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    ok = graphene.Boolean()

    def mutate(root, info, id):
        username = get_jwt_identity()
        user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        db_id = from_global_id(id)[1]
        education = EducationModel.query.get(db_id)
        if education.user != user:
            pass
        db.session.delete(education)
        db.session.commit()

        return DeleteEducationExperience(ok=True)


class Mutation(graphene.ObjectType):
    edit_biographical_data = EditBiographicalData.Field()
    create_address = CreateAddress.Field()
    edit_address = EditAddress.Field()
    delete_address = DeleteAddress.Field()
    create_education_experience = CreateEducationExperience.Field()
    edit_education_experience = EditEducationExperience.Field()
    delete_education_experience = DeleteEducationExperience.Field()
