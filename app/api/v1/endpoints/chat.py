from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from typing import List
from app.api.deps import get_current_user, get_chat_service
from app.schemas.chat import ChatResponse, MessageCreate, MessageResponse, UnreadSummaryResponse
from app.services.chat import ChatService
from app.services.chat_ws_manager import chat_ws_manager
from app.models.users import User

router = APIRouter()

@router.post("/direct/{target_user_id}", response_model=ChatResponse)
async def start_direct_chat(
        target_user_id: int,
        current_user: User = Depends(get_current_user),
        service: ChatService = Depends(get_chat_service)
    ):
    return await service.get_or_create_chat(current_user.id, target_user_id)

@router.get("/", response_model=List[ChatResponse])
async def list_my_chats(
        current_user: User = Depends(get_current_user),
        service: ChatService = Depends(get_chat_service)
    ):
    return await service.get_my_chats(current_user.id)

@router.websocket("/ws/{chat_id}")
async def websocket_chat_endpoint(
        websocket: WebSocket,
        chat_id: int
    ):
    await chat_ws_manager.connect(websocket, chat_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        chat_ws_manager.disconnect(websocket, chat_id)

@router.post("/{chat_id}/messages", response_model=MessageResponse)
async def send_message(
        chat_id: int,
        message_in: MessageCreate,
        current_user: User = Depends(get_current_user),
        service: ChatService = Depends(get_chat_service)
    ):
    new_message = await service.send_message(chat_id, current_user.id, message_in)
    message_data = MessageResponse.model_validate(new_message).model_dump(mode="json")
    await chat_ws_manager.broadcast_to_chat(chat_id, message_data)
    return new_message

@router.get("/{chat_id}/messages", response_model=List[MessageResponse])
async def get_messages(
        chat_id: int,
        skip: int = 0,
        limit: int = 50,
        current_user: User = Depends(get_current_user),
        service: ChatService = Depends(get_chat_service)
    ):
    return await service.get_chat_messages(chat_id, current_user.id, skip, limit)

@router.get("/unread", response_model=UnreadSummaryResponse)
async def get_unread_messages(
        current_user: User = Depends(get_current_user),
        service: ChatService = Depends(get_chat_service)
    ):
    return await service.get_unread_messages_summary(current_user.id)