from fastapi import APIRouter, Depends

from depends import get_post_repository, get_current_user
from models.posts import LIKE_VALUE, DISLIKE_VALUE
from repositories.posts import PostRepository
from schemas.posts import PostIn, Post, EstimationIn, Estimation
from schemas.users import User
from utils.users import check_owner_permission


router = APIRouter()


@router.get("", response_model=list[Post])
async def get_posts(posts: PostRepository = Depends(get_post_repository)):
    return await posts.get_all()


@router.post("", response_model=Post)
async def create_post(
    post: PostIn,
    posts: PostRepository = Depends(get_post_repository),
    user: User = Depends(get_current_user)
):
    return await posts.create(p=post, user_id=user.id)


@router.put("/{post_id}", response_model=Post)
async def edit_post(
    post_id: int,
    post: PostIn,
    posts: PostRepository = Depends(get_post_repository),
    user: User = Depends(get_current_user)
):
    current_post = await posts.get_by_id(post_id)
    await check_owner_permission(obj=current_post, user_id=user.id)
    return await posts.edit(post_id=post_id, p=post, user_id=user.id)


@router.delete("/post_id", response_model=dict)
async def delete_post(
    post_id: int,
    posts: PostRepository = Depends(get_post_repository),
    user: User = Depends(get_current_user)
):
    current_post = await posts.get_by_id(post_id)
    await check_owner_permission(obj=current_post, user_id=user.id)
    return await posts.delete(post_id=post_id)


@router.post("/like", response_model=Estimation)
async def like_post(
    post_id: int,
    posts: PostRepository = Depends(get_post_repository),
    user: User = Depends(get_current_user)
):
    return await posts.set_estimation(EstimationIn(
        post_id=post_id, user_id=user.id, value=LIKE_VALUE
    ))


@router.post("/dislike", response_model=Estimation)
async def dislike_post(
    post_id: int,
    posts: PostRepository = Depends(get_post_repository),
    user: User = Depends(get_current_user)
):
    return await posts.set_estimation(EstimationIn(
        post_id=post_id, user_id=user.id, value=DISLIKE_VALUE
    ))
