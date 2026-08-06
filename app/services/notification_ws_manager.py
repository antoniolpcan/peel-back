from typing import Dict
from fastapi import WebSocket

class NotificationConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_notification(self, user_id: int, notification_data: dict):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json(notification_data)

notification_ws_manager = NotificationConnectionManager()