from typing import List, Optional

from pydantic import BaseModel



class UserBase(BaseModel):
    username: str


class ProfileBase(BaseModel):
    name: str


class ProfileCreate(ProfileBase):
    pass


class Profile(ProfileBase):
    id: int

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: Optional[bool]
    profile: Optional[Profile]

    class Config:
        orm_mode = True


class UserInDb(User):
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str]=None
