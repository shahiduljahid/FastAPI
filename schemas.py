from typing import List
from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    body: str
    published: bool = True


class Blog(BlogBase):
    title: str
    body: str
    published: bool = True

    class Config:
        from_attributes = True


class User(BaseModel):
    name: str
    email: str
    password: str


class UserInfo(BaseModel):

    name: str
    email: str


class ShowUser(BaseModel):

    name: str
    email: str
    blogs: List[Blog] = []

    class Config:
        from_attributes = True


class ShowUserBlog(BaseModel):
    title: str
    body: str
    creator: UserInfo

    class Config:
        from_attributes = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
