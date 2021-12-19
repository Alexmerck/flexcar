import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgres://admin:1q2w3e4r5T@localhost/flexcar_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
