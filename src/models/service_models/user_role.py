import uuid

from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from models.service_models.base import Base


class UserRole(Base):
    __tablename__ = 'user_role'

    id = Column(
        UUID(as_uuid=True), primary_key=True,
        default=uuid.uuid4, unique=True, nullable=False
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'))
    role_id = Column(UUID(as_uuid=True), ForeignKey('role.id'))
    __table_args__ = (
        UniqueConstraint('user_id', 'role_id', name='user_role_uc'),
    )

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f'<Role {self.id} {self.name}>'
