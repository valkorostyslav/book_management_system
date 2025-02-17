from pydantic import BaseModel, EmailStr

class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    password: str

class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: str
    last_name: str

    class Config:
        from_attributes = True

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

