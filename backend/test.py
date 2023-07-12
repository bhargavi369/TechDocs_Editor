import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

env = './.env.local' 
load_dotenv(env)

DB_CONN=os.environ.get('DB_CONN')
DB_NAME=os.environ.get('DB_NAME')
DB_USER=os.environ.get('DB_USER')
DB_PASS=os.environ.get('DB_PASS')
DB_PORT=os.environ.get('DB_PORT')
DB=os.environ.get('DB')

DB_URL = 'mysql+mysqlconnector://' + DB_USER + ':' + DB_PASS + '@' + DB_CONN + ':' + DB_PORT + '/' + DB_NAME # + '?host=' + DB_CONN + '?port=' + DB_PORT
print(DB_URL)


engine = create_engine(url=DB_URL, pool_size=100, max_overflow=0)

engine.connect()

print(engine.connect())

