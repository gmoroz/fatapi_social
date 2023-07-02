from pydantic import BaseModel, EmailStr


class TunedModel(BaseModel):
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase, TunedModel):
    password: str


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase, TunedModel):
    id: int
    owner_id: int


class PostResponse(PostCreate):
    likes: int
    dislikes: int


class Token(BaseModel):
    access_token: str
    token_type: str
