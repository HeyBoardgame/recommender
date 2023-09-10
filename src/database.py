import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

username = os.environ['DB_USERNAME']
password = os.environ['DB_PASSWORD']
host = os.environ['DB_HOST']
port = os.environ['DB_PORT']
database = os.environ['DB_NAME']

SQLAlCHEMY_DATABASE_URL = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'

engine = create_engine(
    SQLAlCHEMY_DATABASE_URL, pool_recycle=500
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
