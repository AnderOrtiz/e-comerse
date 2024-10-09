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
async def car(id: str):
    pipeline = [
        {
            "$match": {"_id": ObjectId(id)}
        },
        {
            "$lookup": {
                "from": "products",
                "localField": "car",
                "foreignField": "_id",
                "as": "products",
            }
        },
        {
            "$project": {
                "_id": 0,
                "name": {"$concat": ["$name", " ", "$last_name"]},
                "email": "$email",
                "gender": "$gender",
                "age": "$age",
                "products": "$products",
                "total": {"$sum": "$products.price" }
            }
        }
    ]

    try:
        results = db_client.users.aggregate(pipeline)
        results_list = list(results)  # Convert cursor to list
        converted_results = convert_objectid(results_list)  # Convert ObjectId to string
        return converted_results
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= {"result": str(e)})


@router.put("/add")
async def add_to_car(id: str, car: str):
    try:
        db_client.users.update_one(
            {"_id": ObjectId(id)}, {"$push": {"car": ObjectId(car)}})
    except Exception as e:
        return {"error": "No se ha actualizado el user", "detail": str(e)}

    return convert_objectid(db_client.users.find_one({"_id": ObjectId(id)}))


@router.put("/remove")
async def remove_to_car(id: str, car: str):
    try:
        db_client.users.update_one(
            {"_id": ObjectId(id)}, {"$pull": {"car": ObjectId(car)}})
    except Exception as e:
        return {"error": "No se ha actualizado el user", "detail": str(e)}

    return convert_objectid(db_client.users.find_one({"_id": ObjectId(id)}))

#66945917fc1a7e13e5ee431f
#669451cc78cca06840498ff4