from pydantic import BaseModel
from typing import Optional


class Product(BaseModel):
    id: Optional[str] = None
    name: str
    price: float
    detail: str
    car: bool




