from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: Optional[str] = None
    name: str
    last_name: str
    email: str


class UserInfo(User):
    gender: str
    age: int


class UserPrivet(UserInfo):
    password: str