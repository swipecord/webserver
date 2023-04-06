from pydantic import BaseModel
from datetime import date


class PublicationBase(BaseModel):
    pass


class PublicationCreate(PublicationBase):
    title: str
    description: str
    text: str


class Publication(PublicationBase):
    title: str
    description: str
    text: str
    id: int
    owner_id: int
    time_created: date
    views_counter: int


    class Config:
        orm_mode = True