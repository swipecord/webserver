from typing import Any, List
from pydantic import BaseModel
from datetime import date


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
    class Config:
        orm_mode: True


class User(UserBase):
    publications: List[Any] = [] # Publication #TODO:
    blacklisted_users: List[Any] = []
    name: str
    email: str
    time_created: date
    id: int

    class Config:
        orm_mode = True


class SearchUserBase(BaseModel):
    pass


class SearchUserByID(SearchUserBase):
    id: int


class SearchUserByName(SearchUserBase):
    name: str


class UserBlacklistBase(BaseModel):
    user_id: int
    blacklisted_user_id: int


class CreateUserBlacklist(UserBlacklistBase):
    pass


class UserBlacklist(UserBlacklistBase):
    id: int

    class Config:
        orm_mode=True