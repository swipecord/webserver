from pydantic import BaseModel


class PublicationBase(BaseModel):
    pass


class PublicationCreate(PublicationBase):
    title: str
    description: str
    text: str
    owner_id: int

class Publication(PublicationBase):
    title: str
    description: str
    text: str
    id: int
    owner_id: int

    class Config:
        orm_mode: True