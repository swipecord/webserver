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
    import time
    start = time.time()
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.post("/users/", response_model=models.User)
def create_user(user: models.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user=user)


def start():
    "Need for poetry"
    uvicorn.run("webserver.main:app", host="127.0.0.1", port=1337, reload=True)
