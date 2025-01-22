from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.db import Base
from app.models.confirmation import confirmation_tag

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    confirmations = relationship(
        "Confirmation",
        secondary=confirmation_tag,
        back_populates="tags",
    )