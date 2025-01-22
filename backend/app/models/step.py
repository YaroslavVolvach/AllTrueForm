from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Step(Base):
    __tablename__ = "steps"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)  
    support_request_id = Column(Integer, ForeignKey('support_requests.id'))

    support_request = relationship("SupportRequest", back_populates="steps")