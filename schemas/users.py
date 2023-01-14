from typing import Optional

from pydantic import BaseModel, EmailStr, constr


class UserIn(BaseModel):
    email: EmailStr
    password: constr(min_length=6)


class User(UserIn):
    id: Optional[int] = None


class UserWithCredentials(BaseModel):
    user: User
    access_token: str
    refresh_token: str
