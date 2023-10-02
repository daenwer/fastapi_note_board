import json
from os import environ

import databases
from sqlalchemy import MetaData, create_engine

DB_USER = environ.get("DB_USER", "user")
DB_PASS = environ.get("DB_PASS", "password")
DB_HOST = environ.get("DB_HOST", "localhost")

if json.loads(environ.get("TESTING").lower()):
    DB_NAME = environ.get("DB_TEST_NAME", "testing_name")
else:
    DB_NAME = environ.get("DB_NAME", "name")


SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
)

database = databases.Database(SQLALCHEMY_DATABASE_URL)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=10,
    max_overflow=2,
    pool_recycle=300,
    pool_pre_ping=True,
    pool_use_lifo=True,
)

metadata = MetaData()
