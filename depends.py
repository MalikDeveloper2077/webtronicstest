from fastapi import Security, Depends
from fastapi_jwt import JwtAuthorizationCredentials

from db import database
from config import access_security
from repositories.posts import PostRepository
from repositories.users import UserRepository
from schemas.users import User


def get_user_repository() -> UserRepository:
    return UserRepository(database)


def get_post_repository() -> PostRepository:
    return PostRepository(database)


async def get_current_user(
    credentials: JwtAuthorizationCredentials = Security(access_security),
    users: UserRepository = Depends(get_user_repository)
) -> User:
    return await users.get_by_email(credentials['email'])
