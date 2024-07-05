from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: Optional[str] = None
    name: str
    last_name: str
    email: str


class UserPrivet(User):
    id: Optional[str] = None
    name: str
    last_name: str
    email: str
    password: str
    gender: str
    age: int