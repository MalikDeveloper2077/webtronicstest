from fastapi import HTTPException

from repositories.base import BaseRepository
from schemas.posts import PostIn, Post, EstimationIn, Estimation
from models.posts import posts, estimations


class PostRepository(BaseRepository):
    async def get_all(self):
        all_posts = await self.database.fetch_all(posts.select())
        return [Post.from_orm(post) for post in all_posts]

    async def get_by_id(self, post_id):
        query = posts.select().where(posts.c.id == post_id)
        post = await self._get_one(query)
        return Post.parse_obj(post)

    async def create(self, p: PostIn, user_id: int):
        post = Post(text=p.text, user_id=user_id)
        values = self._get_schema_db_values(post, ['id'])
        post.id = await self.database.execute(posts.insert().values(**values))
        return post

    async def edit(self, p: PostIn, post_id: int, user_id: int):
        post = Post(id=post_id, text=p.text, user_id=user_id)
        values = self._get_schema_db_values(post, ['id'])
        query = posts.update().where(posts.c.id == post_id).values(**values)
        await self.database.execute(query)
        return post

    async def delete(self, post_id: int):
        query = posts.delete().where(posts.c.id == post_id)
        await self.database.execute(query)
        return {'success': True}

    async def _create_estimation(self, estimation: EstimationIn):
        new_like = Estimation(
            user_id=estimation.user_id,
            post_id=estimation.post_id,
            value=estimation.value
        )
        values = self._get_schema_db_values(new_like, ['id'])
        new_like.id = await self.database.execute(estimations.insert().values(**values))
        return new_like

    async def set_estimation(self, estimation: EstimationIn):
        """Like or dislike post"""
        post = await self.get_by_id(estimation.post_id)
        if post.user_id == estimation.user_id:
            raise HTTPException(400, 'You cannot like/dislike your post')

        try:
            # If the estimation exists, change it
            query = estimations.update().where(
                estimations.c.post_id == estimation.post_id,
                estimations.c.user_id == estimation.user_id
            ).values(value=estimation.value)
            updated_estimation = await self._get_one(query)
            return Estimation.parse_obj(updated_estimation)
        except HTTPException:
            # Estimation doesn't exist, create it
            return await self._create_estimation(estimation)
