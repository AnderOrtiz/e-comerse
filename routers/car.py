from fastapi import APIRouter, HTTPException, status
from db.schemas.order import convert_objectid
from db.client import db_client

router = APIRouter(
    prefix="/car",
    tags=["Car"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}},
)



@router.get("/")
async def car():
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
            "$match": {
                "products.car": False,
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
        return {"result": str(e)}
