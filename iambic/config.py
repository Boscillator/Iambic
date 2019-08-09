class Base:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Development(Base):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../app.sqlite'


class Testing(Base):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
