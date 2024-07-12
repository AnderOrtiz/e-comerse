from pydantic import BaseModel
from typing import Optional


class Order(BaseModel):
    id: Optional[str] = None
    id_user: str
    id_products: list