from fastapi import APIRouter
from app.api.v1.endpoints import posts, users, auth, colors, storage
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(posts.router, prefix="/posts", tags=["Posts"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(colors.router, prefix="/colors", tags=["Colors"])
api_router.include_router(storage.router, prefix="/storage", tags=["Storage"])
