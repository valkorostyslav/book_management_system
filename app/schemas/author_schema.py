from pydantic import BaseModel, Field


class AuthorBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    biography: str = Field(..., min_length=10, max_length=1000)


class AuthorCreate(AuthorBase):
    name: str = Field(..., min_length=2, max_length=100)
    biography: str = Field(..., min_length=10, max_length=1000)


class AuthorResponse(AuthorBase):
    id: int

    class Config:
        from_attributes = True