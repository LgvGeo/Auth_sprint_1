import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models.service_models.base import Base


class Role(Base):
    __tablename__ = 'role'

    id = Column(
        UUID(as_uuid=True), primary_key=True,
        default=uuid.uuid4, unique=True, nullable=False
    )
    name = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    users = relationship('User', secondary='user_role', back_populates='roles')

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f'<Role {self.id} {self.name}>'
