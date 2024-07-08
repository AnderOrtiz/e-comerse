from fastapi import APIRouter, Depends, HTTPException, status
from db.models.user import User, UserPrivet
from db.schemas.user import user_schemas, users_schemas
from db.client import db_client
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITH = "HS256"
ACCESS_TOKEN_DURATION = 1  # en minutos
SECRET = "201d573bd7d1344d3a3bfce1550b69102fd11be3db6d379508b6cccc58ea230b"

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"])

# Entidad user
users_db = users_schemas(db_client.users.find())

def search_user_db(name: str) -> UserPrivet:
    # Asegúrate de que name se encuentra en users_db
    user = db_client.users.find_one({"name": name})
    if user:
        return UserPrivet(**user)  # Ajusta si UserPrivet tiene un constructor adecuado
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

async def auth_user(token: str = Depends(oauth2_scheme)) -> UserPrivet:
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITH])
        name = payload.get("sub")
        if name is None:
            raise exception
        user = search_user_db(name)
    except JWTError:
        raise exception

    return user

async def current_user(user: UserPrivet = Depends(auth_user)) -> UserPrivet:
    # Se elimina la validación del campo `disable` ya que no está presente en la base de datos.
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = search_user_db(form.username)  # Cambia 'form.name' a 'form.username'

    if not crypt.verify(form.password, user_db.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_DURATION)
    access_token = jwt.encode(
        {"sub": user_db.name, "exp": datetime.utcnow() + access_token_expires},
        SECRET,
        algorithm=ALGORITH
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
async def me(user: UserPrivet = Depends(current_user)) -> UserPrivet:
    return user
