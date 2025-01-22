from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class SupportRequest(Base):
    __tablename__ = "support_requests"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    issue_type = Column(String, nullable=False)

    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=True)
    tag = relationship("Tag", back_populates="support_requests")