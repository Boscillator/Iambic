import logging

class Base:
    DICTIONARY_PATH = 'data/cmudict-0.7b.txt'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOGGING_LEVEL = logging.INFO


class Development(Base):
    DEBUG = True
    TESTING = False
    LOGGING_LEVEL = logging.DEBUG
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../app.sqlite'


class Testing(Development):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
