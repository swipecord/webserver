from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .database import Base
from config import text_length, title_length, description_length

class Publication(Base):
    __tablename__ = "publications"

    id = Column(Integer, primary_key=True)
    title = Column(String(title_length))
    text = Column(String(text_length))
    description = Column(String(description_length))
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="publications")
    time_created = Column(DateTime(timezone=True), server_default=func.now())