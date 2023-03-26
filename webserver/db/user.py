from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

email_length = 32
name_length = 16
password_length = 32

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(email_length), unique=True, index=True)
    name = Column(String(name_length), index=True)
    password = Column(String(password_length))
    publications = relationship("Publication", back_populates="owner")