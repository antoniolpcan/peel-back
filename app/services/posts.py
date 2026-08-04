from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.posts import PostRepository
from app.repositories.post_likes import PostLikeRepository
from app.schemas.post import PostUpdate, PostCreate, PostQueryParams
from app.models.posts import Post

class PostService:
    def __init__(self, db: AsyncSession):
        self.post_repo = PostRepository(db)
        self.like_repo = PostLikeRepository(db)

    async def create_post(self, post_in: PostCreate, user_id: int) -> Post:
        post = await self.post_repo.create(post_in=post_in, user_id=user_id)
        post.is_liked = False
        return post

    async def get_post_by_id(self, post_id: int, current_user_id: int | None = None) -> Post:
        post = await self.post_repo.get_by_id(post_id=post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Post não encontrado."
            )
        if current_user_id:
            existing_like = await self.like_repo.get_like(user_id=current_user_id, post_id=post.id)
            post.is_liked = existing_like is not None
        else:
            post.is_liked = False

        return post

    async def search_posts(self, params: PostQueryParams, current_user_id: int | None = None) -> list[Post]:
        posts = await self.post_repo.search(**vars(params))
        if current_user_id and posts:
            post_ids = [p.id for p in posts]
            liked_post_ids = await self.like_repo.get_user_liked_post_ids(user_id=current_user_id, post_ids=post_ids)
            for post in posts:
                post.is_liked = post.id in liked_post_ids
        else:
            for post in posts:
                post.is_liked = False

        return posts
    
    async def update_post(self, post_id: int, post_in: PostUpdate, user_id: int) -> Post:
        post = await self.get_post_by_id(post_id=post_id, current_user_id=user_id)
        if post.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para atualizar este post."
            )
        return await self.post_repo.update(db_obj=post, post_in=post_in)

    async def delete_post(self, post_id: int, user_id: int) -> bool:
        post = await self.get_post_by_id(post_id=post_id)
        if post.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Você não tem permissão para apagar este post."
            )
        return await self.post_repo.delete(db_obj=post)

    async def toggle_post_like(self, post_id: int, user_id: int) -> Post:
        post = await self.get_post_by_id(post_id=post_id, current_user_id=user_id)
        existing_like = await self.like_repo.get_like(user_id=user_id, post_id=post_id)
        
        if existing_like:
            await self.like_repo.delete(existing_like)
            await self.post_repo.decrement_likes(post)
            post.is_liked = False
        else:
            await self.like_repo.create(user_id=user_id, post_id=post_id)
            await self.post_repo.increment_likes(post)
            post.is_liked = True 

        return post