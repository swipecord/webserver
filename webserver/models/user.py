from typing import Any, List
from pydantic import BaseModel



class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    password: str
    name: str
    email: str

class UserLoginDataUsingToken(UserBase):
    id: int
    token: str


class UserLoginDataUsingPassword(UserBase):
    email: str
    password: str


class UserFullLoginData(UserLoginDataUsingToken, UserLoginDataUsingPassword):
    pass


class User(UserBase):
    publications: List[Any] = [] # Publication #TODO:
    name: str
    email: str
    id: int

    class Config:
        orm_mode = True



class SearchUserBase(BaseModel):
    pass


class SearchUserByID(SearchUserBase):
    id: int


class SearchUserByName(SearchUserBase):
    name: str

    
