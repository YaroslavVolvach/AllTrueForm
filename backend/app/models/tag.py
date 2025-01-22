from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.database import Base

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    support_requests = relationship("SupportRequest", back_populates="tag")