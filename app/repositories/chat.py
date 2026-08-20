from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.chat import Chat, ChatMember, Message
from app.models.users import User

class ChatRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_direct_chat(self, user1_id: str, user2_id: str) -> Chat | None:
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

    async def create_direct_chat(self, user1_id: str, user2_id: str) -> Chat:
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

    async def get_user_chats(self, user_id: str) -> list[Chat]:
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

    async def is_member(self, chat_id: str, user_id: str) -> bool:
        stmt = select(ChatMember).where(
            ChatMember.chat_id == chat_id,
            ChatMember.user_id == user_id
        )
        result = await self.db.scalar(stmt)
        return result is not None

    async def create_message(self, chat_id: str, sender_id: str, content: str) -> Message:
        msg = Message(chat_id=chat_id, sender_id=sender_id, content=content)
        self.db.add(msg)
        await self.db.commit()
        await self.db.refresh(msg)
        return msg

    async def get_messages(self, chat_id: str, skip: int = 0, limit: int = 50) -> list[Message]:
        stmt = (
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(Message.created_at.asc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.scalars(stmt)
        return list(result.all())

    async def get_unread_messages_summary(self, user_id: str) -> dict:
        stmt = (
            select(User, func.count(Message.id).label("unread_count"))
            .join(Message, Message.sender_id == User.id)
            .join(ChatMember, ChatMember.chat_id == Message.chat_id)
            .where(
                ChatMember.user_id == user_id,
                Message.sender_id != user_id,
                Message.is_read == False
            )
            .group_by(User.id)
            .options(selectinload(User.avatar))
        )
        
        result = await self.db.execute(stmt)
        rows = result.all()

        senders = [
            {
                "user": user,
                "unread_count": unread_count
            }
            for user, unread_count in rows
        ]
        
        total_unread = sum(item["unread_count"] for item in senders)

        return {
            "total_unread": total_unread,
            "senders": senders
        }

    async def mark_messages_as_read(self, chat_id: str, user_id: str) -> None:
        stmt = (
            update(Message)
            .where(
                Message.chat_id == chat_id,
                Message.sender_id != user_id,
                Message.is_read == False
            )
            .values(is_read=True)
        )
        await self.db.execute(stmt)
        await self.db.commit()