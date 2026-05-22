from fastapi import APIRouter, WebSocket
from app.services.websocket_service import websocket_handler

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_handler(websocket)