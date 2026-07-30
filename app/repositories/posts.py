from sqlalchemy.ext.asyncio import AsyncSession
from app.models.posts import Post
from app.schemas.post import PostUpdate
from app.schemas.enums import PostSortField, SortOrder
from sqlalchemy import select

class PostRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, post_id: int) -> Post | None:
        return await self.db.scalar(select(Post).where(Post.id == post_id))

    async def get_multi(self, skip: int = 0, limit: int = 100) -> list[Post]:
        result = await self.db.scalars(select(Post).offset(skip).limit(limit))
        return list(result.all())
    
    async def search(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        title: str | None = None,
        body: str | None = None,
        user_id: int | None = None,
        order_by: PostSortField = PostSortField.created_at,
        sort_order: SortOrder = SortOrder.desc
    ) -> list[Post]:
        
        stmt = select(Post)
        if title:
            stmt = stmt.where(Post.title.ilike(f"%{title}%")) 
        if body:
            stmt = stmt.where(Post.body.ilike(f"%{body}%")) 
        if user_id:
            stmt = stmt.where(Post.user_id == user_id)

        sort_column = getattr(Post, order_by.value)
        if sort_order == SortOrder.desc:
            sort_column = sort_column.desc()
        else:
            sort_column = sort_column.asc()
        stmt = stmt.order_by(sort_column).offset(skip).limit(limit)
        result = await self.db.scalars(stmt)
        return list(result.all())
    
    async def create(self, post_in: Post, user_id: int) -> Post:
        db_obj = Post(
            title=post_in.title,
            body=post_in.body,
            color_id=post_in.color_id,
            user_id=user_id
        )
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: Post, post_in: PostUpdate) -> Post:
        update_data = post_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj
        
    async def delete(self, db_obj: Post) -> bool:
        try:
            await self.db.delete(db_obj)
            await self.db.commit()
            return True
        except Exception:
            await self.db.rollback()
            return False

    async def increment_likes(self, post: Post) -> None:
        post.likes += 1
        self.db.add(post)
        await self.db.commit()
        await self.db.refresh(post)

    async def decrement_likes(self, post: Post) -> None:
        post.likes = max(0, post.likes - 1)
        self.db.add(post)
        await self.db.commit()
        await self.db.refresh(post)