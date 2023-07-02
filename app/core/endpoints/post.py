from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_session
from app.core.models import Post, User
from app.core.schemas import PostBase, PostCreate

post_router = APIRouter(tags=["posts"])


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


@post_router.get("/posts/{post_id}", response_model=PostCreate)
async def read_post(post_id: int, db: AsyncSession = Depends(get_session)):
    if db_post := (await db.get(Post, post_id)):
        return db_post
    raise HTTPException(status_code=404, detail="Post not found")


@post_router.put("/posts/{post_id}", response_model=PostCreate)
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
    return db_post


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
