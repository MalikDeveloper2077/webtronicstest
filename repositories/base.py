from databases import Database
from fastapi import HTTPException
from pydantic import BaseModel


class BaseRepository:
    def __init__(self, database: Database):
        self.database = database

    @staticmethod
    def _get_schema_db_values(schema: BaseModel, to_remove: list[str]):
        values = {**schema.dict()}
        for field in to_remove:
            values.pop(str(field), None)
        return values

    async def _get_one(self, query):
        obj = await self.database.fetch_one(query)
        if not obj:
            raise HTTPException(400, 'Object is not found')
        return obj
