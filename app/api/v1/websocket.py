from typing import Dict, Set

from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect

router = APIRouter(prefix="/ws", tags=["WebSockets"])

class ConnectionManager:
    def __init__(self):
        # user_id -> WebSocket
        self.active_connections: Dict[int, Set[WebSocket]] = {}
        # chat_room_id -> set of user_ids (현재 해당 방을 보고 있는 유저들)
        self.room_status: Dict[int, Dict[int, int]] = {}

    async def connect(self, websocket: WebSocket, user_id: int, chat_room_id: int):
        await websocket.accept()
        user_connections = self.active_connections.setdefault(user_id, set())
        user_connections.add(websocket)

        room_connections = self.room_status.setdefault(chat_room_id, {})
        room_connections[user_id] = room_connections.get(user_id, 0) + 1

    def disconnect(self, websocket: WebSocket, user_id: int, chat_room_id: int):
        user_connections = self.active_connections.get(user_id)
        if user_connections:
            user_connections.discard(websocket)
            if not user_connections:
                del self.active_connections[user_id]

        room_connections = self.room_status.get(chat_room_id)
        if room_connections and user_id in room_connections:
            room_connections[user_id] -= 1
            if room_connections[user_id] <= 0:
                del room_connections[user_id]
            if not room_connections:
                del self.room_status[chat_room_id]

    def is_user_in_room(self, user_id: int, chat_room_id: int) -> bool:
        """특정 유저가 현재 해당 채팅방을 보고 있는지 확인"""
        return self.room_status.get(chat_room_id, {}).get(user_id, 0) > 0

    async def broadcast_to_user(self, user_id: int, message: dict):
        """특정 유저에게 실시간 이벤트 전송"""
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            try:
                await websocket.send_json(message)
            except Exception:
                # 연결이 끊겼을 가능성이 있으면 무시 (나중에 disconnect에서 처리됨)
                pass

# 싱글톤 매니저 객체
async def _connect(self, websocket: WebSocket, user_id: int, chat_room_id: int):
    await websocket.accept()

    user_connections = self.active_connections.setdefault(user_id, set())
    user_connections.add(websocket)

    room_connections = self.room_status.setdefault(chat_room_id, {})
    room_connections[user_id] = room_connections.get(user_id, 0) + 1


def _disconnect(self, websocket: WebSocket, user_id: int, chat_room_id: int):
    user_connections = self.active_connections.get(user_id)
    if user_connections:
        user_connections.discard(websocket)
        if not user_connections:
            del self.active_connections[user_id]

    room_connections = self.room_status.get(chat_room_id)
    if room_connections and user_id in room_connections:
        room_connections[user_id] -= 1
        if room_connections[user_id] <= 0:
            del room_connections[user_id]
        if not room_connections:
            del self.room_status[chat_room_id]


def _is_user_in_room(self, user_id: int, chat_room_id: int) -> bool:
    return self.room_status.get(chat_room_id, {}).get(user_id, 0) > 0


async def _broadcast_to_user(self, user_id: int, message: dict):
    stale_connections = []

    for websocket in list(self.active_connections.get(user_id, set())):
        try:
            await websocket.send_json(message)
        except Exception:
            stale_connections.append(websocket)

    if not stale_connections:
        return

    user_connections = self.active_connections.get(user_id)
    if not user_connections:
        return

    for websocket in stale_connections:
        user_connections.discard(websocket)

    if not user_connections:
        del self.active_connections[user_id]


async def _broadcast_to_room(
    self,
    chat_room_id: int,
    message: dict,
    exclude_user_ids: Set[int] | None = None,
):
    exclude_user_ids = exclude_user_ids or set()

    for user_id in list(self.room_status.get(chat_room_id, {})):
        if user_id in exclude_user_ids:
            continue
        await self.broadcast_to_user(user_id, message)


ConnectionManager.connect = _connect
ConnectionManager.disconnect = _disconnect
ConnectionManager.is_user_in_room = _is_user_in_room
ConnectionManager.broadcast_to_user = _broadcast_to_user
ConnectionManager.broadcast_to_room = _broadcast_to_room


manager = ConnectionManager()

@router.websocket("/chats/{chat_room_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    chat_room_id: int,
    user_id: int = Query(..., alias="user_id")
):
    # 연결 수락 및 상태 등록
    await manager.connect(websocket, user_id, chat_room_id)
    
    try:
        while True:
            # 클라이언트로부터 메시지를 기다림 (주로 연결 유지용)
            await websocket.receive_text()
            # 필요하다면 여기서 클라이언트의 액션을 처리할 수도 있습니다.
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id, chat_room_id)
