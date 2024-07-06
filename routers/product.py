from fastapi import APIRouter, HTTPException, status
from db.models.product import Product
from db.schemas.product import product_schemas, products_schemas
from db.client import db_client

router = APIRouter(prefix="/product",
                    tags=["Product"],
                    responses={status.HTTP_404_NOT_FOUND:{"message": "No encontrado"}})

@router.get("/", response_model=list[Product])
async def all_user():
    return products_schemas(db_client.products.find())
