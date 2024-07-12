from fastapi import APIRouter, HTTPException, status
from db.models.order import Order
from db.schemas.order import convert_objectid
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/order",
                    tags=["Order"],
                    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})


def search_orders(key, value):
    return db_client.orders.find_one({key: value})


@router.get("/", responses={status.HTTP_200_OK: {"message": "Ok"}})
async def all_orders():
    pipeline = [
        {
            "$lookup": {
                "from": "users",
                "localField": "id_user",
                "foreignField": "_id",
                "as": "user",
            }
        },
        {"$unwind": "$user"},
        {
            "$lookup": {
                "from": "products",
                "localField": "id_products",
                "foreignField": "_id",
                "as": "products",
            }
        },
        {
            "$project": {
                "_id": 0,
                "user": "$user",
                "products": "$products"
            }
        }
    ]

    try:
        results = db_client.orders.aggregate(pipeline)
        results_list = list(results)  # Convert cursor to list
        converted_results = convert_objectid(results_list)  # Convert ObjectId to string
        return converted_results
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= {"result": str(e)})



@router.get("/{id}", response_model=Order, status_code=status.HTTP_200_OK)
async def product(id: str):
    order = search_orders("_id", ObjectId(id))
    return convert_objectid(order)


@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_product(order: Order):
    existing_user = search_orders("_id", order.id)
    if isinstance(existing_user, Order):
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"El order ya existe")

    order_dict = dict(order)
    order_dict["id_user"] = ObjectId(order_dict["id_user"])
    order_dict["id_products"] = [ObjectId(id) for id in order_dict["id_products"]]
    
    del order_dict["id"]

    id = db_client.orders.insert_one(order_dict).inserted_id

    new_order = convert_objectid(db_client.orders.find_one({"_id": id}))

    return Order(**new_order)


@router.put("/", status_code=status.HTTP_200_OK, response_model=Order)
async def update_product(order: Order):
    order_dict = dict(order)
    order_dict["id_user"] = ObjectId(order_dict["id_user"])
    order_dict["id_products"] = [ObjectId(id) for id in order_dict["id_products"]]
    
    del order_dict["id"]

    try:
        result = db_client.orders.find_one_and_replace(
            {"_id": ObjectId(order.id)}, order_dict)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No se ha actualizado la orden")

    return convert_objectid(search_orders("_id", ObjectId(order.id)))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id:str):
    found = db_client.orders.find_one_and_delete({"_id":ObjectId(id)})
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Product Not found")

#668dbc4247d6b10825495cab   