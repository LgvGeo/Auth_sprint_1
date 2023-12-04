import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from models.service_models.base import Base


class UsersHistory(Base):
    __tablename__ = 'user_history'
    id = Column(
        UUID(as_uuid=True), primary_key=True,
        default=uuid.uuid4, unique=True, nullable=False
    )
    user_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    action = Column(String(255), nullable=False)

    def __init__(self, user_id: str, action: str) -> None:
        self.user_id = user_id
        self.action = action

    def __repr__(self) -> str:
        return f'<UserHistory {self.id} {self.user_id} {self.action}>'
