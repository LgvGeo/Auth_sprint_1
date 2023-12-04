from pydantic import BaseModel


class RoleGrantRevokeRequestModel(BaseModel):
    user_id: str
    role: str


class RoleCreateRequestModel(BaseModel):
    name: str
