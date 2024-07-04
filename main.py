from fastapi import FastAPI
from db.models.user import User
from db.schemas.user import user_schemas, users_schemas
from db.client import db_client
app = FastAPI()




@app.get("/", response_model=list[User])
async def all_user():
    return users_schemas(db_client.users.find())




#https://fastapi.tiangolo.com/

#https://pymongo.readthedocs.io/en/stable/examples/index.html

#https://github.com/AnderOrtiz/e-comerse