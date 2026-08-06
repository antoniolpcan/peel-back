from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.chat import ChatRepository
from app.schemas.chat import MessageCreate
from app.models.chat import Chat, Message

class ChatService:
    def __init__(self, db: AsyncSession):
        self.chat_repo = ChatRepository(db)

    async def get_or_create_chat(self, current_user_id: int, target_user_id: int) -> Chat:
        if current_user_id == target_user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Você não pode criar um chat com você mesmo."
            )
            
        conv = await self.chat_repo.get_direct_chat(current_user_id, target_user_id)
        if conv:
            return conv
        return await self.chat_repo.create_direct_chat(current_user_id, target_user_id)

    async def get_my_chats(self, user_id: int) -> list[Chat]:
        return await self.chat_repo.get_user_chats(user_id)

    async def send_message(self, chat_id: int, sender_id: int, message_in: MessageCreate) -> Message:
        is_member = await self.chat_repo.is_member(chat_id, sender_id)
        if not is_member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não faz parte desta conversa."
            )
        return await self.chat_repo.create_message(
            chat_id=chat_id, 
            sender_id=sender_id, 
            content=message_in.content
        )

    async def get_chat_messages(self, chat_id: int, user_id: int, skip: int, limit: int) -> list[Message]:
        is_member = await self.chat_repo.is_member(chat_id, user_id)
        if not is_member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para ler esta conversa."
            )
        return await self.chat_repo.get_messages(chat_id, skip, limit)