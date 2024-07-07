from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from db.models.user import User, UserInfo, UserPrivet
from db.models.auth import Token, CreateUserRequest
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

router = APIRouter(
    prefix="/auth",
    tags= ["Auth"],
)

ACCESS_TOKEN_DURATION = 3
SECRET_KEY = "201d573bd7d1344d3a3bfce1550b69102fd11be3db6d379508b6cccc58ea230b"
ALGORITH = "HS256"


bcrypt_context = CryptContext(schemes=["bcrypt"])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest):
    pass