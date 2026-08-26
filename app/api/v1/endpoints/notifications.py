from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from typing import List

from app.api.deps import get_notification_service, get_current_user, get_websocket_user
from app.schemas.notifications import NotificationResponse, NotificationCreate
from app.services.notifications import NotificationService
from app.services.notification_ws_manager import notification_ws_manager
from app.models.users import User

router = APIRouter()

@router.websocket("/ws")
async def websocket_notifications_endpoint(
        websocket: WebSocket,
        current_user: User = Depends(get_websocket_user)
    ):
    await notification_ws_manager.connect(websocket, current_user.id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        notification_ws_manager.disconnect(current_user.id)

@router.post("/", response_model=NotificationResponse)
async def create_notification(
        data: NotificationCreate,
        current_user: User = Depends(get_current_user),
        service: NotificationService = Depends(get_notification_service)
    ):
    new_notification = await service.create_notification(data, actor_id=current_user.id)
    notification_data = NotificationResponse.model_validate(new_notification).model_dump(mode="json")
    await notification_ws_manager.send_personal_notification(
        user_id=new_notification.user_id, 
        notification_data=notification_data
    )
    return new_notification

@router.get("/me", response_model=List[NotificationResponse])
async def list_notifications(
        skip: int = 0,
        limit: int = 20,
        current_user: User = Depends(get_current_user),
        service: NotificationService = Depends(get_notification_service)
    ):
    return await service.get_user_notifications(current_user.id, skip, limit)


@router.patch("/{notification_id}/read", response_model=NotificationResponse)
async def mark_as_read(
        notification_id: str,
        current_user: User = Depends(get_current_user),
        service: NotificationService = Depends(get_notification_service)
    ):
    return await service.read_notification(notification_id, user_id=current_user.id)