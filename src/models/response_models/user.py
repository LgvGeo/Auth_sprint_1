import uuid

from pydantic import BaseModel


class UserSignInResponseModel(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    email: str


class UserResponseModel(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    roles: list[str]


class UserUpdateResponseModel(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    email: str
