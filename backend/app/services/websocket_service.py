from fastapi import WebSocket
from app.agents.voice_agent import process_user_query

async def websocket_handler(websocket: WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_text()

        response = process_user_query(data)

        await websocket.send_text(response)