from fastapi import APIRouter, HTTPException, status, Depends
from db.models.user import User, UserInfo, UserPrivet
from db.schemas.user import user_schemas, users_schemas, convert_objectid
from db.client import db_client
from bson import ObjectId
from routers.auth import current_user  # Importa current_user desde auth.py

router = APIRouter(prefix="/user",
                    tags=["User"],
                    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})


@router.get("/", response_model=list[UserPrivet])
async def all_user():
    return convert_objectid(users_schemas(db_client.users.find()))


@router.get("/{id}", response_model=UserPrivet, status_code=status.HTTP_200_OK)
async def user(id: str):
    user = db_client.users.find_one({"_id": ObjectId(id)})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return  convert_objectid(user)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserPrivet):
    existing_user = db_client.users.find_one({"email": user.email })
    if isinstance(existing_user, UserPrivet):
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                            detail=f"El usuario {user.name} ya existe")

    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = convert_objectid(db_client.users.find_one({"_id": id}))

    return User(**new_user)


@router.put("/", status_code=status.HTTP_200_OK, response_model=User)
async def update_user(user: UserInfo):
    user_dict = dict(user)
    user_id = user_dict.pop("id")

    try:
        update_result = db_client.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": user_dict}
        )
        if update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")

    updated_user = db_client.users.find_one({"_id": ObjectId(user_id)})
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found after update")
    return updated_user


@router.put("/password", status_code=status.HTTP_200_OK)
# Agregar dependencia
async def update_password(id: str, password: str, user: UserPrivet = Depends(current_user)):
    try:
        db_client.users.update_one(
            {"_id": ObjectId(id)}, {"$set": {"password": password}})
    except Exception as e:
        return {"error": "No se ha actualizado el user", "detail": str(e)}

    return convert_objectid(db_client.users.find_one({"_id": ObjectId(id)}))    


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Not found")
