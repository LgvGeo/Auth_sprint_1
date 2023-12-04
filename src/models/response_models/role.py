from pydantic import BaseModel


class RoleCreateResponseModel(BaseModel):
    id: str
    name: str
