class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1Aangels-@localhost:5432/Db_Server'
    SECRET_KEY = 'random1'


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = 'random2'
