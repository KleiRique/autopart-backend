from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active: dict[str, WebSocket] = {}

    async def connect(self, conv_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active[conv_id] = websocket

    def disconnect(self, conv_id: str):
        self.active.pop(conv_id, None)

    async def send(self, conv_id: str, data: dict):
        ws = self.active.get(conv_id)
        if ws:
            await ws.send_json(data)

manager = ConnectionManager()
