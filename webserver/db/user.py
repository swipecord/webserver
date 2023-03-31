from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .database import Base
from config import email_length, name_length, password_length, token_length


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    token = Column(String(token_length), unique=True)
    email = Column(String(email_length), unique=True)
    name = Column(String(name_length))
    password = Column(String(password_length))
    publications = relationship("Publication", back_populates="owner")
    time_created = Column(DateTime(timezone=True), server_default=func.now())