from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.post_repository import PostItRepository
from app.schemas.post import PostItCreate, PostItUpdate
from app.models.post import PostIt

class PostItService:
    def __init__(self, db: AsyncSession):
        self.post_repo = PostItRepository(db)

    async def check_if_post_exists(self,post_id):
        post = await self.post_repo.get_by_id(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Post-It não encontrado."
            )
        return post

    async def create_post(self, post_in: PostItCreate, user_id: int) -> PostIt:
        return await self.post_repo.create(post_in)

    async def list_posts(self, skip: int, limit: int) -> list[PostIt]:
        return await self.post_repo.get_multi(skip=skip, limit=limit)

    async def toggle_like(self, post_id: int, user_id: int) -> PostIt:
        post = await self.check_if_post_exists(post_id)
        if post.has_liked:
            post.likes -= 1
            post.has_liked = False
        else:
            post.likes += 1
            post.has_liked = True
        await self.post_repo.save()
        return post
    
    async def update_post(self, post_id: int, post_in: PostItUpdate) -> PostIt:
        post = await self.check_if_post_exists(post_id)
        return await self.post_repo.update(db_obj=post, post_in=post_in)

    async def delete_post(self, post_id: int, user_id: int) -> bool:
        post = await self.check_if_post_exists(post_id)
        if post.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Você não tem permissão para apagar este post."
            )
        return await self.post_repo.delete(db_obj=post)