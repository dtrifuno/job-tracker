import os
from subprocess import check_call

def dev():
    env = dict(os.environ)
    env['FLASK_DEBUG'] = "True"
    env['FLASK_ENV'] = "development"
    check_call(["flask", "run"], env=env)