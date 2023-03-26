from typing import Any, List
from pydantic import BaseModel



class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    name: str


class User(UserBase):
    publications: List[Any] = [] # Publication #TODO:
    name: str
    id: int

    class Config:
        orm_mode = True


class SearchUserBase(BaseModel):
    pass


class SearchUserByID(SearchUserBase):
    id: int


class SearchUserByName(SearchUserBase):
    name: str