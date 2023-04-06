from typing import (Annotated, Generator,
                    Union, List)

from fastapi import (FastAPI, HTTPException, 
                     Depends,  Header)

from sqlalchemy.orm import Session
import uvicorn


# TODO: refactoring .models.user module
from . import db, crud, models
from .db.database import Base, engine, SessionLocal
from config import (NAME_LENGTH, TEXT_LENGTH,
                    TITLE_LENGTH, DESCRIPTION_LENGTH,
                    EMAIL_LENGTH, PASSWORD_LENGTH)

Base.metadata.create_all(bind=engine)
app = FastAPI()


# Dependency
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/", response_model=List[models.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/publication/{publ_id}/", response_model=models.Publication)
def get_publication_by_id(publ_id: int, db: Session = Depends(get_db)) -> db.Publication:
    publ = crud.get_publication_by_id(db, publ_id)
    if publ is None:
        raise HTTPException(status_code=404)
    return publ


@app.get("/user/{user_id}/", response_model=models.Publication)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)) -> db.User:
    user = crud.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404)
    return user


@app.get("/user/{user_id}/publications/", response_model=List[models.Publication])
def get_user_publications(user_id: int, db: Session = Depends(get_db)) -> List[db.Publication]:
    user = crud.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404)
    return user.publications


@app.get("/publication/{publication_id}/author/", response_model=models.User)
def get_publication_author(publication_id: int, db: Session = Depends(get_db)) -> db.User:
    publ = crud.get_publication_by_id(db, publication_id)
    if publ is None:
        raise HTTPException(status_code=404)
    return publ.owner


@app.get("/me/view/", response_model=dict[str, List[models.Publication]])
def get_publication_view(user_id: Annotated[int, Header()],
                         user_token: Annotated[str, Header()],
                         db: Session = Depends(get_db)) -> dict[str, List[int]]:
    if not crud.check_user_token(db, user_id, user_token):
        raise HTTPException(status_code=403)
    return {"view": list(crud.get_user_view(db, user_id))}


@app.get("/me/blacklist/")
def get_user_blacklist(user_id: Annotated[int, Header()],
                       user_token: Annotated[str, Header()],
                       db: Session = Depends(get_db)) -> dict[str, List[int]]:
    if not crud.check_user_token(db, user_id, user_token):
        raise HTTPException(status_code=403)
    return {"blacklist": list(crud.get_user_blacklist(db, user_id))} # cast tuple to list


@app.post("/create/user/", response_model=models.UserFullLoginData)
def create_user(user: models.UserCreate, db: Session = Depends(get_db)) -> models.UserFullLoginData:
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    created_user = crud.create_user(db, user=user)
    user_dict = created_user.__dict__
    user_dict.pop("_sa_instance_state")  # remove unnecessary attribute
    return models.UserFullLoginData(**user_dict)
      

@app.post("/create/publication/", response_model=models.Publication)
def create_publication(user_id: Annotated[int, Header()],
                       user_token: Annotated[str, Header()],
                       publication: models.PublicationCreate, 
                       db: Session = Depends(get_db)) -> db.Publication:
    if not crud.check_user_token(db, user_id, user_token):
        raise HTTPException(status_code=403)
    return crud.create_user_publication(db, publication, user_id)

    
@app.post("/me/blacklist/add/{blacklisted_user_id}/", response_model=models.UserBlacklist)
def add_user_to_blacklist(user_id: Annotated[int, Header()],
                          user_token: Annotated[str, Header()],
                          blacklisted_user_id: int,
                          db: Session = Depends(get_db)) -> db.UserBlacklist:
    if not crud.check_user_token(db, user_id, user_token) or user_id==blacklisted_user_id:
        raise HTTPException(status_code=403)

    blacklist = crud.add_user_to_blacklist(db, models.CreateUserBlacklist(
        user_id=user_id, 
        blacklisted_user_id=blacklisted_user_id
        )
    )
    if blacklist is None:
        raise HTTPException(status_code=404)
    
    return blacklist


def start():
    "Need for poetry"

    # This code is literally works 1 out of 2 times, 
    # I think it's better than doing it regularly anyway. 
    # If you have any ideas how this can be improved, please email me.
    from sys import platform
    from config import ISDOCKER

    if not ISDOCKER and platform == "linux":
        from os import system
        print("Running: sudo lsof -t -i tcp:8000 | xargs kill -9 (fix [Errno 98] linux issue)")
        system("sudo lsof -t -i tcp:8000 | xargs kill -9")

    uvicorn.run("webserver.main:app", host="127.0.0.1", port=8000, reload=True)