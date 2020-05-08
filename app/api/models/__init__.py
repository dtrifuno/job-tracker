from flask_sqlalchemy import SQLAlchemy, Model


class ModelClass(Model):

    def update(self, kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


db = SQLAlchemy(model_class=ModelClass)


from .profile import User, Profile, Address, Education, WorkExperience  # noqa
