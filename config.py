class Config(object):
    DEBUG = True
    SECRET_KEY = '21f1006869'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SESSION_PERMANENT = False
    SESSION_TYPE = 'filesystem'
    