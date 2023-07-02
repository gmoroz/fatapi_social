from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_session
from app.core.models import Post, User
from app.core.schemas import PostBase, PostCreate, PostResponse
from app.db import redis_db

post_router = APIRouter(tags=["posts"])


async def count_post_likes_dislikes(post_id: int):
    redis_key = f"post:{post_id}"
    ratings = await redis_db.hvals(redis_key)
    ratings = [rating.decode("utf-8") for rating in ratings]
    likes = ratings.count("1")
    dislikes = ratings.count("-1")
    return likes, dislikes


@post_router.post("/posts", response_model=PostCreate)
async def create_post(
    post: PostBase,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    db_post = Post(**post.dict(), owner_id=current_user.id)
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post


@post_router.get("/posts/{post_id}", response_model=PostResponse)
async def read_post(post_id: int, db: AsyncSession = Depends(get_session)):
    db_post = await db.get(Post, post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    likes, dislikes = await count_post_likes_dislikes(post_id)

    return PostResponse(**db_post.__dict__, likes=likes, dislikes=dislikes)


@post_router.put("/posts/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post: PostBase,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    db_post = await db.get(Post, post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db_post.title = post.title
    db_post.content = post.content
    await db.commit()
    await db.refresh(db_post)

    likes, dislikes = await count_post_likes_dislikes(post_id)

    return PostResponse(**db_post.__dict__, likes=likes, dislikes=dislikes)


@post_router.delete("/posts/{post_id}")
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    db_post = await db.get(Post, post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    await db.delete(db_post)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@post_router.post("/posts/{post_id}/like")
async def like_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    db_post = await db.get(Post, post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.owner_id == current_user.id:
        raise HTTPException(status_code=403, detail="User cannot like his own post")

    redis_key = f"post:{post_id}"
    user_rating = await redis_db.hget(redis_key, str(current_user.id))
    if user_rating is not None:
        user_rating = user_rating.decode("utf-8")

    if user_rating == "1":
        await redis_db.hdel(redis_key, str(current_user.id))
        return {"message": "Like removed"}
    else:
        await redis_db.hset(redis_key, str(current_user.id), "1")
        return {"message": "Post liked"}


@post_router.post("/posts/{post_id}/dislike")
async def dislike_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    db_post = await db.get(Post, post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.owner_id == current_user.id:
        raise HTTPException(status_code=403, detail="User cannot dislike his own post")

    redis_key = f"post:{post_id}"
    user_rating = await redis_db.hget(redis_key, str(current_user.id))
    if user_rating is not None:
        user_rating = user_rating.decode("utf-8")

    if user_rating == "-1":
        await redis_db.hdel(redis_key, str(current_user.id))
        return {"message": "Dislike removed"}
    else:
        await redis_db.hset(redis_key, str(current_user.id), "-1")
        return {"message": "Post disliked"}
