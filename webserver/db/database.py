from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import \
(
    DBTYPE, DBDRIVER, DBUSER, 
    DBPASSWORD, DBHOST, DBNAME
)


SQLALCHEMY_DATABASE_URL = f"{DBTYPE}+{DBDRIVER}://{DBUSER}:{DBPASSWORD}@{DBHOST}/{DBNAME}?charset=utf8mb4"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()