from typing import List, Union
from sqlalchemy.orm import Session

from webserver import models, db
from config import token_length
from webserver.libs.token_generator import generate_token

def get_user_by_id(session: Session, user_id: int) -> Union[db.User, None]:
    return session.query(db.User).filter(db.User.id == user_id).first()


def get_user_by_email(session: Session, email: str) -> Union[db.User, None]:
    return session.query(db.User).filter(db.User.email == email).first()


def get_users(session: Session, skip: int = 0, limit: int = 100) -> List[db.User]:
    return session.query(db.User).offset(skip).limit(limit).all()


def create_user(session: Session, user: models.UserCreate) -> db.User:
    hashed_password = user.password  # TODO: hash function
    token = generate_token(token_length)
    while session.query(db.User).filter(db.User.token == token).first():
        token = generate_token(token_length)

    db_user = db.User(email=user.email, name=user.name, password=hashed_password, token=token)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def check_user_token(session: Session, user_id: int, user_token: str) -> Union[bool, None]:
    db_user = session.query(db.User).filter(db.User.id == user_id).first()
    if db_user is None:
        return None
    return db_user.token == user_token


def get_publication_by_id(session: Session, publication_id: int):
    return session.query(db.Publication).filter(db.Publication.id == publication_id).first()


def get_publications(session: Session, skip: int = 0, limit: int = 100) -> List[db.Publication]:
    return session.query(db.Publication).offset(skip).limit(limit).all()


def create_user_publication(session: Session, publication: models.PublicationCreate, user_id: int) -> db.Publication:
    db_item = db.Publication(**publication.dict(), owner_id=user_id)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item