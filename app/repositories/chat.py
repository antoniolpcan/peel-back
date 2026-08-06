from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.chat import Chat, ChatMember, Message
from app.models.users import User

class ChatRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_direct_chat(self, user1_id: int, user2_id: int) -> Chat | None:
        stmt = (
            select(Chat)
            .join(ChatMember, Chat.id == ChatMember.chat_id)
            .where(ChatMember.user_id.in_([user1_id, user2_id]))
            .group_by(Chat.id)
            .having(func.count(ChatMember.id) == 2)
            .options(
                selectinload(Chat.members)
                .selectinload(ChatMember.user)
                .selectinload(User.avatar)
            )
        )
        result = await self.db.execute(stmt)
        chats = result.scalars().all()
        for conv in chats:
            member_ids = {m.user_id for m in conv.members}
            if member_ids == {user1_id, user2_id}:
                return conv
        return None

    async def create_direct_chat(self, user1_id: int, user2_id: int) -> Chat:
        conv = Chat()
        self.db.add(conv)
        await self.db.flush()
        
        member1 = ChatMember(chat_id=conv.id, user_id=user1_id)
        member2 = ChatMember(chat_id=conv.id, user_id=user2_id)
        self.db.add_all([member1, member2])
        
        await self.db.commit()

        stmt = (
            select(Chat)
            .where(Chat.id == conv.id)
            .options(
                selectinload(Chat.members)
                .selectinload(ChatMember.user)
                .selectinload(User.avatar)
            )
        )
        return await self.db.scalar(stmt)

    async def get_user_chats(self, user_id: int) -> list[Chat]:
        stmt = (
            select(Chat)
            .join(ChatMember)
            .where(ChatMember.user_id == user_id)
            .options(
                selectinload(Chat.members)
                .selectinload(ChatMember.user)
                .selectinload(User.avatar)
            )
            .order_by(Chat.created_at.desc())
        )
        result = await self.db.scalars(stmt)
        return list(result.all())

    async def is_member(self, chat_id: int, user_id: int) -> bool:
        stmt = select(ChatMember).where(
            ChatMember.chat_id == chat_id,
            ChatMember.user_id == user_id
        )
        result = await self.db.scalar(stmt)
        return result is not None

    async def create_message(self, chat_id: int, sender_id: int, content: str) -> Message:
        msg = Message(chat_id=chat_id, sender_id=sender_id, content=content)
        self.db.add(msg)
        await self.db.commit()
        await self.db.refresh(msg)
        return msg

    async def get_messages(self, chat_id: int, skip: int = 0, limit: int = 50) -> list[Message]:
        stmt = (
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(Message.created_at.asc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.scalars(stmt)
        return list(result.all())