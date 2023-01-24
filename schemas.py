import pydantic as _pydantic
import datetime as _datetime


class UserBase(_pydantic.BaseModel):
    email: str
    name: str
    phone: str


class Config:
    orm_mode = True


class UserRequest(UserBase):
    password_hash: str

    Config = Config()


class UserResponse(UserBase):
    id: int
    created_at: _datetime.datetime

    Config = Config()


class PostBase(_pydantic.BaseModel):
    post_title: str
    post_description: str
    image: str


class PostRequest(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    user_id: str
    created_at: _datetime.datetime

    Config = Config()
