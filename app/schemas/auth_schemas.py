from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


class TokenDataSchema(BaseModel):
    username: str | None = None


class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
