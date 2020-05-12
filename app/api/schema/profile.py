from graphql import GraphQLError
from graphql_relay import from_global_id

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from flask_graphql_auth import get_jwt_identity, query_header_jwt_required, mutation_header_jwt_required

from . import get_user

from app.api.models import db
from app.api.models import User as UserModel, \
    Profile as ProfileModel, \
    Address as AddressModel, \
    Education as EducationModel, \
    Skill as SkillModel, \
    WorkExperience as WorkExperienceModel, \
    PersonalProject as PersonalProjectModel


def get_from_gid(gid):
    type_name, id = from_global_id(gid)
    type_to_model = {
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


class SkillType(SQLAlchemyObjectType):
    class Meta:
        model = SkillModel
        interfaces = (relay.Node,)


class WorkExperienceType(SQLAlchemyObjectType):
    class Meta:
        model = WorkExperienceModel
        interfaces = (relay.Node,)


class PersonalProjectType(SQLAlchemyObjectType):
    class Meta:
        model = PersonalProjectModel
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    profile = graphene.Field(ProfileType)
    addresses = graphene.List(AddressType)
    education = graphene.List(EducationType)
    skills = graphene.List(SkillType)
    work_history = graphene.List(WorkExperienceType)
    personal_projects = graphene.List(PersonalProjectType)

    @query_header_jwt_required
    def resolve_profile(self, info):
        user = get_user()
        return user.profile

    @query_header_jwt_required
    def resolve_addresses(self, info):
        user = get_user()
        return user.addresses

    @query_header_jwt_required
    def resolve_education(self, info):
        user = get_user()
        return user.education

    @query_header_jwt_required
    def resolve_skills(self, info):
        user = get_user()
        return user.skills

    @query_header_jwt_required
    def resolve_work_history(self, info):
        user = get_user()
        return user.work_history

    @query_header_jwt_required
    def resolve_personal_projects(self, info):
        user = get_user()
        return user.personal_projects

class BiographicalDataInput(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    phone_number = graphene.String()
    website_url = graphene.String()
    github_url = graphene.String()
    linkedin_url = graphene.String()


class EditBiographicalData(graphene.Mutation):
    class Arguments:
        biographical_data_data = BiographicalDataInput(required=True)

    profile = graphene.Field(ProfileType)

    @mutation_header_jwt_required
    def mutate(root, info, biographical_data_data):
        user = get_user()
        profile = user.profile
        profile.update(biographical_data_data)
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
        user = get_user()
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
        address = get_from_gid(id)
        address.update(address_data)
        db.session.commit()
        return EditAddress(address=address)


class DeleteAddress(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    ok = graphene.Boolean()

    @mutation_header_jwt_required
    def mutate(root, info, id):
        address = get_from_gid(id)
        db.session.delete(address)
        db.session.commit()
        return DeleteAddress(ok=True)


class EducationExperienceInput(graphene.InputObjectType):
    school = graphene.String()
    location = graphene.String()
    degree_and_field = graphene.String()
    gpa = graphene.String()
    date_from = graphene.String()
    date_to = graphene.String()
    description = graphene.String()


class CreateEducationExperience(graphene.Mutation):
    class Arguments:
        education_experience_data = EducationExperienceInput(required=True)

    education_experience = graphene.Field(EducationType)

    @mutation_header_jwt_required
    def mutate(root, info, education_experience_data):
        user = get_user()
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
        education = get_from_gid(id)
        education.update(education_experience_data)
        db.session.commit()
        return EditEducationExperience(education_experience=education)


class DeleteEducationExperience(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    ok = graphene.Boolean()

    @mutation_header_jwt_required
    def mutate(root, info, id):
        education = get_from_gid(id)
        db.session.delete(education)
        db.session.commit()
        return DeleteEducationExperience(ok=True)


class SkillInput(graphene.InputObjectType):
    skill = graphene.String()
    category = graphene.String()


class CreateSkill(graphene.Mutation):
    class Arguments:
        skill_data = SkillInput(required=True)

    skill = graphene.Field(SkillType)

    @mutation_header_jwt_required
    def mutate(root, info, skill_data):
        user = get_user()
        skill = SkillModel(user=user, **skill_data)
        db.session.add(skill)
        db.session.commit()
        return CreateSkill(skill=skill)


class EditSkill(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        skill_data = SkillInput(required=True)

    skill = graphene.Field(SkillType)

    @mutation_header_jwt_required
    def mutate(root, info, id, skill_data):
        skill = get_from_gid(id)
        skill.update(skill_data)
        db.session.commit()
        return EditSkill(skill=skill)


class DeleteSkill(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    ok = graphene.Boolean()

    @mutation_header_jwt_required
    def mutate(root, info, id):
        skill = get_from_gid(id)
        db.session.delete(skill)
        db.session.commit()
        return DeleteSkill(ok=True)



class WorkExperienceInput(graphene.InputObjectType):
    company = graphene.String()
    position = graphene.String()
    location = graphene.String()
    date_from = graphene.String()
    date_to = graphene.String()
    description = graphene.String()


class CreateWorkExperience(graphene.Mutation):
    class Arguments:
        work_experience_data = WorkExperienceInput(required=True)

    work_experience = graphene.Field(WorkExperienceType)

    @mutation_header_jwt_required
    def mutate(root, info, work_experience_data):
        user = get_user()
        work_experience = WorkExperienceModel(
            user=user, **work_experience_data)
        db.session.add(work_experience)
        db.session.commit()
        return CreateWorkExperience(work_experience=work_experience)


class EditWorkExperience(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        work_experience_data = WorkExperienceInput(required=True)

    work_experience = graphene.Field(WorkExperienceType)

    @mutation_header_jwt_required
    def mutate(root, info, id, work_experience_data):
        work = get_from_gid(id)
        work.update(work_experience_data)
        db.session.commit()
        return EditWorkExperience(work_experience=work)


class DeleteWorkExperience(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    ok = graphene.Boolean()

    @mutation_header_jwt_required
    def mutate(root, info, id):
        work = get_from_gid(id)
        db.session.delete(work)
        db.session.commit()

        return DeleteWorkExperience(ok=True)


class PersonalProjectInput(graphene.InputObjectType):
    project_name = graphene.String()
    url = graphene.String()
    description = graphene.String()


class CreatePersonalProject(graphene.Mutation):
    class Arguments:
        personal_project_data = PersonalProjectInput(required=True)

    personal_project = graphene.Field(PersonalProjectType)

    @mutation_header_jwt_required
    def mutate(root, info, personal_project_data):
        user = get_user()
        print(user)
        print(personal_project_data)
        personal_project = PersonalProjectModel(
            user=user, **personal_project_data)
        print(personal_project)
        db.session.add(personal_project)
        db.session.commit()
        return CreatePersonalProject(personal_project=personal_project)


class EditPersonalProject(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        personal_project_data = PersonalProjectInput(required=True)

    personal_project = graphene.Field(PersonalProjectType)

    @mutation_header_jwt_required
    def mutate(root, info, id, personal_project_data):
        personal_project = get_from_gid(id)
        personal_project.update(personal_project_data)
        db.session.commit()
        return EditPersonalProject(personal_project=personal_project)


class DeletePersonalProject(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    ok = graphene.Boolean()

    @mutation_header_jwt_required
    def mutate(root, info, id):
        personal_project = get_from_gid(id)
        db.session.delete(personal_project)
        db.session.commit()

        return DeletePersonalProject(ok=True)


class Mutation(graphene.ObjectType):
    edit_biographical_data = EditBiographicalData.Field()
    create_address = CreateAddress.Field()
    edit_address = EditAddress.Field()
    delete_address = DeleteAddress.Field()
    create_education_experience = CreateEducationExperience.Field()
    edit_education_experience = EditEducationExperience.Field()
    delete_education_experience = DeleteEducationExperience.Field()
    create_skill = CreateSkill.Field()
    edit_skill = EditSkill.Field()
    delete_skill = DeleteSkill.Field()
    create_work_experience = CreateWorkExperience.Field()
    edit_work_experience = EditWorkExperience.Field()
    delete_work_experience = DeleteWorkExperience.Field()
    create_personal_project = CreatePersonalProject.Field()
    edit_personal_project = EditPersonalProject.Field()
    delete_personal_project = DeletePersonalProject.Field()
