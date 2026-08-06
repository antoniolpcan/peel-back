from fastapi import APIRouter
from app.api.v1.endpoints import posts, users, auth, colors, storage, follows, notifications, chat, user_settings
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(posts.router, prefix="/posts", tags=["Posts"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(user_settings.router, prefix="/user_settings", tags=["User Settings"])
api_router.include_router(follows.router, prefix="/follows", tags=["Follows"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
api_router.include_router(colors.router, prefix="/colors", tags=["Colors"])
api_router.include_router(storage.router, prefix="/storage", tags=["Storage"])
