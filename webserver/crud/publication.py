from typing import List, Union
from sqlalchemy.orm import Session

from webserver import models, db


def get_publication_by_id(session: Session, publication_id: int) -> Union[db.Publication, None]:
    return session.query(db.Publication).filter(db.Publication.id == publication_id).first()


def get_publications(session: Session, skip: int = 0, limit: int = 100) -> List[db.Publication]:
    return session.query(db.Publication).offset(skip).limit(limit).all()


def create_user_publication(session: Session, publication: models.PublicationCreate, user_id: int) -> db.Publication:
    db_item = db.Publication(**publication.dict(), owner_id=user_id)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item