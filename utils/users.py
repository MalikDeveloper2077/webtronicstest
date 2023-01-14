from fastapi import HTTPException

from config import access_security, refresh_security
from schemas.users import User


def create_jwt_response(user: User, subject=None):
    if not subject:
        subject = {'id': user.id, 'email': user.email}

    return {
        'user': user,
        'access_token': access_security.create_access_token(subject=subject),
        'refresh_token': refresh_security.create_refresh_token(subject=subject)
    }


async def check_owner_permission(obj, user_id: int):
    if obj.user_id != user_id:
        raise HTTPException(403, 'You are not post owner')
