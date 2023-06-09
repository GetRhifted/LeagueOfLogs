from fastapi import APIRouter
from pydantic import BaseModel
from utils.jwt_manager import create_token
from fastapi.responses import JSONResponse
from schemas.user import User

user_router = APIRouter()


@user_router.post('/Login', tags=['Auth'])
def login(user: User):
    if user.email == 'megustaellol@gamil.com' and user.password == 'admin':
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)