from flask import Flask
from flask_graphql import GraphQLView

from app.api.schema.schema import schema
from app.api.models import db

from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    app.add_url_rule(
        "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True))

    return app
