import os
from subprocess import check_call

def dev():
    env = dict(os.environ)
    env['FLASK_DEBUG'] = "True"
    env['FLASK_ENV'] = "development"
    check_call(["flask", "run"], env=env)

def create_dev_db():
    env = dict(os.environ)
    env['FLASK_DEBUG'] = "True"
    env['FLASK_ENV'] = "development"
    check_call(["flask", "db", "init"], env=env)
    check_call(["flask", "db", "migrate"], env=env)
    check_call(["flask", "db", "upgrade"], env=env)

def create_prod_db():
    env = dict(os.environ)
    env['FLASK_DEBUG'] = "False"
    env['FLASK_ENV'] = "production"
    check_call(["flask", "db", "init"], env=env)
    check_call(["flask", "db", "migrate"], env=env)
    check_call(["flask", "db", "upgrade"], env=env)