from pydantic import BaseModel
from typing import Optional, List

class User(BaseModel):
    id: Optional[str] = None
    name: str
    last_name: str
    email: str

class UserInfo(User):
    gender: str
    age: int

class UserPrivet(UserInfo):
    car: Optional[List[str]] = None
    password: str
