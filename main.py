from fastapi import FastAPI, APIRouter
from routers import user


app = FastAPI()

app.include_router(user.router)






#https://fastapi.tiangolo.com/

#https://pymongo.readthedocs.io/en/stable/examples/index.html

#https://github.com/AnderOrtiz/e-comerse