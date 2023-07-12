from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import yaml
import os
from dotenv import load_dotenv

# basedir = os.path.abspath(os.path.dirname(__file__))
env = './.env.local' # os.path.join('./.env.local')

# if os.path.exists(env):
load_dotenv(env)

DB_CONN=os.environ.get('DB_CONN')
DB_NAME=os.environ.get('DB_NAME')
DB_USER=os.environ.get('DB_USER')
DB_PASS=os.environ.get('DB_PASS')
DB_PORT=os.environ.get('DB_PORT')
DB=os.environ.get('DB')

DB_URL = 'mysql+mysqlconnector://' + DB_USER + ':' + DB_PASS + '@' + DB_CONN + ':' + DB_PORT + '/' + DB_NAME # + '?host=' + DB_CONN + '?port=' + DB_PORT
print(DB_URL)
# else:
#     print('ENV NOT FOUND!!!')

def get_connection():
    return create_engine(url=DB_URL, pool_size=100, max_overflow=0)

def session_factory():
    Base.metadata.create_all(engine)
    return SessionFactory()

# Create a new session
engine         = get_connection()
SessionFactory = sessionmaker(bind=engine)
Base           = declarative_base()