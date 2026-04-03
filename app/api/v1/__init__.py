from fastapi import APIRouter

from app.api.v1 import auth, chats, images, notifications, posts, transactions, users, websocket

router = APIRouter()
router.include_router(auth.router)
router.include_router(users.router)
router.include_router(posts.router)
router.include_router(chats.router)
router.include_router(transactions.router)
router.include_router(notifications.router)
router.include_router(websocket.router)
router.include_router(images.router)
