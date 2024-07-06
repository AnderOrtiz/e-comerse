from fastapi import APIRouter, HTTPException, status
from db.models.product import Product
from db.schemas.product import product_schemas, products_schemas
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/product",
                    tags=["Product"],
                    responses={status.HTTP_404_NOT_FOUND:{"message": "No encontrado"}})

@router.get("/", response_model=list[Product])
async def all_products():
    return products_schemas(db_client.products.find())


@router.get("/{id}", response_model= Product, status_code=status.HTTP_200_OK)
async def product(id:str):
    return search_product("_id", ObjectId(id))


@router.post("/",response_model=Product ,status_code=status.HTTP_201_CREATED)
async def create_product(product:Product):

    existing_user = search_product("_id", product.id)
    if isinstance(existing_user, Product):
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail= f"El usuario {product.name} ya existe")

    product_dict = dict(product)
    del product_dict["id"]

    id = db_client.products.insert_one(product_dict).inserted_id

    new_user = product_schemas(db_client.products.find_one({"_id": id}))

    return Product(**new_user)


@router.put("/", status_code=status.HTTP_200_OK, response_model=Product)
async def update_product(product: Product):

    product_dict = dict(product)
    del product_dict["id"]

    try:
        db_client.products.find_one_and_replace(
            {"_id": ObjectId(product.id)}, product_dict)

    except:
        return {"erro": "No se ha actualizado el producto"}

    return search_product("_id", ObjectId(product.id))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id:str):
    found = db_client.products.find_one_and_delete({"_id":ObjectId(id)})
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Product Not found")


def search_product(fild: str, key):
    try:
        product = db_client.products.find_one({fild: key})
        return Product(**product_schemas(product))
    except:
        return {"message": "Product Not Found"}