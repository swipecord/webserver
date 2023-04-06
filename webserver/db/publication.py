from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .database import Base
from config import TEXT_LENGTH, TITLE_LENGTH, DESCRIPTION_LENGTH


class Publication(Base):
    __tablename__ = "publications"

    id = Column(Integer, primary_key=True)
    title = Column(String(TITLE_LENGTH))
    text = Column(String(TEXT_LENGTH))
    description = Column(String(DESCRIPTION_LENGTH))
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="publications")
    views = relationship("UserView", backref="publication")
    views_counter = Column(Integer, default=1)
    time_created = Column(DateTime(timezone=True), server_default=func.now())