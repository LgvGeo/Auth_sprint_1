import uuid
from datetime import datetime

from passlib.hash import pbkdf2_sha512
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType

from models.service_models.base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(
        UUID(as_uuid=True), primary_key=True,
        default=uuid.uuid4, unique=True, nullable=False
    )
    email = Column(EmailType, unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    roles = relationship(
        'Role', secondary='user_role',
        back_populates='users', lazy='joined'
    )

    def __init__(
            self, email: str, password: str,
            first_name: str, last_name: str
    ) -> None:
        self.email = email
        self.password = pbkdf2_sha512.hash(password)
        self.first_name = first_name
        self.last_name = last_name

    def check_password(self, password: str) -> bool:
        return pbkdf2_sha512.verify(password, self.password)

    def hash_password(self, password: str):
        return pbkdf2_sha512.hash(password)

    def __repr__(self) -> str:
        return f'<User {self.email}>'
