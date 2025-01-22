from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db import Base

confirmation_tag = Table(
    "confirmation_tag",
    Base.metadata,
    Column("confirmation_id", Integer, ForeignKey("confirmations.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
)

class Confirmation(Base):
    __tablename__ = "confirmations" 

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    issue_type = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    user = relationship("User", back_populates="confirmations")

    tags = relationship(
        "Tag",
        secondary=confirmation_tag,
        back_populates="confirmations",
    )

    steps = relationship(
        "Step",
        back_populates="confirmation",
        cascade="all, delete-orphan",
    )