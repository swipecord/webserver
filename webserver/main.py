from typing import Generator, Union, List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import uvicorn

from . import db, crud, models
from .db.database import Base, engine, SessionLocal


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


@app.get("/publication/{publ_id}", response_model=models.Publication)
def get_publication_by_id(publ_id: int, db: Session = Depends(get_db)):
    publ = crud.get_publication_by_id(db, publ_id)
    if publ is None:
        raise HTTPException(status_code=404)
    return publ


@app.get("/user/{user_id}/publications", response_model=List[models.Publication])
def get_user_publications(user_id: int, db: Session = Depends(get_db)) -> List[db.Publication]:
    user = crud.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404)
    return user.publications


@app.post("/create/user/", response_model=models.UserFullLoginData)
def create_user(user: models.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    created_user = crud.create_user(db, user=user)
    user_dict = created_user.__dict__
    user_dict.pop("_sa_instance_state")  # remove unnecessary attribute
    return models.UserFullLoginData(**user_dict)
      

@app.post("/create/publication/", response_model=models.Publication)
def create_publication(user: models.UserLoginDataUsingToken, 
                       publication: models.PublicationCreate, 
                       db: Session = Depends(get_db)):
    
    if crud.check_user_token(db, user.id, user.token):
        return crud.create_user_publication(db, publication, user.id)
    
    raise HTTPException(status_code=403)
    


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
        system(b"sudo lsof -t -i tcp:8000 | xargs kill -9")

    uvicorn.run("webserver.main:app", host="0.0.0.0", port=8000, reload=True)