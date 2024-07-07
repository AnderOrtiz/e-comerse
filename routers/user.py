from fastapi import APIRouter, HTTPException, status
from db.models.user import User, UserInfo ,UserPrivet
from db.schemas.user import user_schemas, users_schemas
from db.client import db_client
from bson import ObjectId   



router = APIRouter(prefix="/user",
                    tags=["User"],
                    responses={status.HTTP_404_NOT_FOUND:{"message": "No encontrado"}})


@router.get("/", response_model=list[User])
async def all_user():
    return users_schemas(db_client.users.find())


@router.get("/{id}", response_model= User, status_code=status.HTTP_200_OK)
async def user(id:str):
    return search_user("_id", ObjectId(id))


@router.post("/",response_model=User ,status_code=status.HTTP_201_CREATED)
async def create_user(user:UserPrivet):

    existing_user = search_user("email", user.email)
    if isinstance(existing_user, UserPrivet):
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail= f"El usuario {user.name} ya existe")
    
    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schemas(db_client.users.find_one({"_id": id}))

    return User(**new_user)


@router.put("/", status_code=status.HTTP_200_OK, response_model=User)
async def update_user(user: UserInfo):

    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict)

    except:
        return {"erro": "No se ha actualizado el user"}

    return search_user("_id", ObjectId(user.id))


@router.put("/password", status_code=status.HTTP_200_OK)
async def update_password(id: str, password: str):
    try:
        db_client.users.update_one(
            {"_id": ObjectId(id)}, {"$set": {"password": password}})
    except Exception as e:
        return {"error": "No se ha actualizado el user", "detail": str(e)}
    
    return search_user("_id", ObjectId(id))



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id:str):
    found = db_client.users.find_one_and_delete({"_id":ObjectId(id)})
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"User Not found")


def search_user(fild: str, key):
    try:
        user = db_client.users.find_one({fild: key})
        return UserPrivet(**user_schemas(user))
    except:
        return {"message": "User Not Found"}