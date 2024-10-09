from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user, product, auth, car, order

app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost:5500",  # Cambia esto al origen de tu frontend
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todos los encabezados
)

app.include_router(user.router)
app.include_router(product.router)
app.include_router(auth.router)
app.include_router(car.router)
app.include_router(order.router)

@app.get("/", tags=["Home"])
def read_root():
    return {"Hello": "World"}




#https://fastapi.tiangolo.com/

#https://pymongo.readthedocs.io/en/stable/examples/index.html

#https://github.com/AnderOrtiz/e-comerse