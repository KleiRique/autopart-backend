from fastapi import WebSocket, WebSocketDisconnect

class WSManager:
    def __init__(self):
        self.active = {}

    async def connect(self, cid: str, ws: WebSocket):
        await ws.accept()
        self.active[cid] = ws

    def disconnect(self, cid: str):
        self.active.pop(cid, None)

    async def send(self, cid: str, data: dict):
        ws = self.active.get(cid)
        if ws:
            await ws.send_json(data)

manager = WSManager()
