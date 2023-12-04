from pydantic import BaseModel, EmailStr, Field


class UserSignInRequestModel(BaseModel):
    email: EmailStr
    password: str
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)


class UserLogInRequestModel(BaseModel):
    email: EmailStr
    password: str


class UserUpdateRequestModel(BaseModel):
    id: str
    email: EmailStr | None = Field(default=None)
    password: str | None = Field(default=None)
    first_name: str | None = Field(default=None, max_length=50)
    last_name: str | None = Field(default=None, max_length=50)
