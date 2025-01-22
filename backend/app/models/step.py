from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Step(Base):
    __tablename__ = "steps"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    confirmation_id = Column(Integer, ForeignKey('confirmations.id', ondelete="CASCADE"))

    confirmation = relationship("Confirmation", back_populates="steps")