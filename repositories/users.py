from fastapi import HTTPException

from repositories.base import BaseRepository

from schemas.users import User, UserIn
from models.users import users


class UserRepository(BaseRepository):
    async def get_by_email(self, email: str) -> User:
        query = users.select().where(users.c.email == email)
        user = await self._get_one(query)
        return User.parse_obj(user)

    async def authenticate(self, u: UserIn) -> (bool, User):
        """Check is account data valid"""
        user = await self.get_by_email(u.email)
        return user.password == u.password, user

    async def create(self, u: UserIn) -> User:
        user = User(
            email=u.email,
            password=u.password
        )
        values = self._get_schema_db_values(user, ['id'])
        query = users.insert().values(**values)
        user.id = await self.database.execute(query)
        return user
