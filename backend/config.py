import os
from dotenv import load_dotenv

# basedir = os.path.abspath(os.path.dirname(__file__))
env = '/.env.local' # os.path.join(basedir,'/.env.local')
# if os.path.exists(env):
load_dotenv(env)

class Config(object):
    DEBUG=False

class DevConfig(Config):
    FLASK_ENV='developement'
    TESTING=True
    DEBUG=True
    SECRET=os.environ.get('SECRET')
    DB_CONN=os.environ.get('DB_CONN')
    DB_NAME=os.environ.get('DB_NAME')
    DB_USER=os.environ.get('DB_USER')
    DB_PASS=os.environ.get('DB_PASS')
    DB_PORT=os.environ.get('DB_PORT')
    DB=os.environ.get('DB')
    DIR_ROOT=os.environ.get('DIR_ROOT')
    DIR_DATA=os.environ.get('DIR_DATA')
    DIR_LOG=os.environ.get('DIR_LOG')

class ProdConfig(Config):
    FLASK_ENV='production'
    TESTING=True
    DEBUG=False
    SECRET=os.environ.get('SECRET')
    DIR_ROOT=os.environ.get('DIR_ROOT')
    DIR_DATA=os.environ.get('DIR_DATA')
    DIR_LOG=os.environ.get('DIR_LOG')
    PGKEY_RID=os.environ.get('R_ID')
    PGKEY_RKEY=os.environ.get('R_KEY')
