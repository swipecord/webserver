from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .database import Base
from config import EMAIL_LENGTH, NAME_LENGTH, PASSWORD_LENGTH, TOKEN_LENGTH


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    token = Column(String(TOKEN_LENGTH), unique=True)
    email = Column(String(EMAIL_LENGTH), unique=True)
    name = Column(String(NAME_LENGTH))
    password = Column(String(PASSWORD_LENGTH))
    publications = relationship("Publication", back_populates="owner")
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    blacklisted_users = relationship("UserBlacklist", backref="user")
    views = relationship("UserView", backref="user")


class UserView(Base):
    __tablename__ = "user_view"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    view_time = Column(DateTime(timezone=True), server_default=func.now())
    publication_id = Column(Integer, ForeignKey('publications.id'), nullable=False)



class UserBlacklist(Base):
    __tablename__ = "user_blacklist"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    blacklisted_user_id = Column(Integer, nullable=False)