from fastapi import APIRouter, HTTPException, status
from db.schemas.order import convert_objectid
from db.client import db_client
from bson import ObjectId

router = APIRouter(
    prefix="/car",
    tags=["Car"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}},
)


@router.get("/", responses={status.HTTP_302_FOUND: {"message": "No encontrado"}})
async def car(id:str):
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
        },#668c6cf258c55a452488c509
        {
            "$match": {
                "user._id" : ObjectId(id),
                "products.car": True,
            }
        },
        {
            "$project": {
                "_id": 0,
                "user": "$user",
                "products": "$products",
                "total": {"$sum": "$products.price" }
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


@router.put("/")
async def add_to_car(id: str, car: bool):
    try:
        db_client.products.update_one(
            {"_id": ObjectId(id)}, {"$set": {"car": car}})
    except Exception as e:
        return {"error": "No se ha actualizado el user", "detail": str(e)}

    return convert_objectid(db_client.orders.find_one({"_id": id}))