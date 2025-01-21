from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.base import Base

support_request_tags = Table(
    'support_request_tags',
    Base.metadata,
    Column('support_request_id', Integer, ForeignKey('support_requests.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)