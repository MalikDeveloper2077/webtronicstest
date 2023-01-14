from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi_jwt import JwtAuthorizationCredentials

from config import refresh_security
from depends import get_user_repository
from repositories.users import UserRepository
from schemas.users import User, UserIn, UserWithCredentials
from utils.users import create_jwt_response


router = APIRouter()


@router.post("/register", response_model=UserWithCredentials)
async def create_user(user: UserIn, users: UserRepository = Depends(
    get_user_repository
)):
    user = await users.create(u=user)
    return create_jwt_response(user)


@router.post("/login", response_model=UserWithCredentials)
async def login(user: UserIn, users: UserRepository = Depends(
    get_user_repository
)):
    is_valid, user = await users.authenticate(u=user)
    if not is_valid:
        raise HTTPException(400, 'Invalid password')
    return create_jwt_response(user)


@router.post("/refresh", response_model=UserWithCredentials)
async def refresh_token(
    credentials: JwtAuthorizationCredentials = Security(refresh_security),
    users: UserRepository = Depends(get_user_repository)
):
    user = await users.get_by_email(credentials.subject['email'])
    return create_jwt_response(user, subject=credentials.subject)
