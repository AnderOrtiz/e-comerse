from fastapi import FastAPI
from routers import user, product, auth,car


app = FastAPI()

app.include_router(user.router)
app.include_router(product.router)
app.include_router(auth.router)
app.include_router(car.router)

@app.get("/", tags=["Home"])
def read_root():
    return {"Hello": "World"}




#https://fastapi.tiangolo.com/

#https://pymongo.readthedocs.io/en/stable/examples/index.html

#https://github.com/AnderOrtiz/e-comerse