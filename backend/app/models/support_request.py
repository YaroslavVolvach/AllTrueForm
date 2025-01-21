from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.enums import RequestStatus
from .support_request_tags import support_request_tags

class SupportRequest(Base):
    __tablename__ = "support_requests"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, index=True)
    issue_type = Column(String)
    status = Column(Enum(RequestStatus), default=RequestStatus.pending)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    tags = relationship("Tag", secondary=support_request_tags)
    user = relationship("User", back_populates="support_requests")

