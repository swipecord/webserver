from typing import List, Union
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from webserver import models, db
from config import TOKEN_LENGTH, PUBL_TIME_SHOWS
from webserver.libs.token_generator import generate_token


def get_user_by_id(session: Session, user_id: int) -> Union[db.User, None]:
    return session.query(db.User).filter(db.User.id == user_id).first()


def get_user_by_email(session: Session, email: str) -> Union[db.User, None]:
    return session.query(db.User).filter(db.User.email == email).first()


def get_users(session: Session, skip: int = 0, limit: int = 100) -> List[db.User]:
    return session.query(db.User).offset(skip).limit(limit).all()


def create_user(session: Session, user: models.UserCreate) -> db.User:
    hashed_password = user.password  # TODO: hash function
    token = generate_token(TOKEN_LENGTH)

    while session.query(db.User).filter(db.User.token == token).first():
        token = generate_token(TOKEN_LENGTH)

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


def add_user_to_blacklist(session: Session, blacklist: models.CreateUserBlacklist) -> Union[db.UserBlacklist, None]:
    db_user = session.query(db.User).filter(db.User.id == blacklist.user_id).first()
    db_blacklisted_user = session.query(db.User).filter(db.User.id == blacklist.blacklisted_user_id).first()

    if db_user is None or db_blacklisted_user is None:
        return None
    
    db_blacklist_item = db.UserBlacklist(**blacklist.__dict__)
    session.add(db_blacklist_item)
    session.commit()
    session.refresh(db_blacklist_item)
    return db_blacklist_item

def get_user_blacklist(session: Session, user_id: int):
    db_user = session.query(db.User).filter(db.User.id == user_id).first()

    if db_user is None:
        return None
    
    return session.query(db.UserBlacklist.blacklisted_user_id).filter(db.UserBlacklist.user_id == user_id).first()


def get_user_view(session: Session, user_id: int) -> List[db.Publication]:
    "Return user publication view"


    def get_recent_publications(session: Session) -> List[db.Publication]:
        # Calculate the date from which to filter publications
        days_ago = datetime.now() - timedelta(days=PUBL_TIME_SHOWS)

        # Request to get a list of publications created no later than {config.PUBL_TIME_SHOWS} days ago
        publications = session.query(db.Publication).\
            filter(db.Publication.time_created >= days_ago).\
            all()

        return publications


    return get_recent_publications(session)