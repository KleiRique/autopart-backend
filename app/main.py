from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.settings import settings
from app.routes import users, stores, conversations, scraping, waha
from app.ws import manager

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "*" if settings.DEBUG else settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(stores.router, prefix="/api/stores", tags=["stores"])
app.include_router(conversations.router, prefix="/api/conversations", tags=["conversations"])
app.include_router(scraping.router, prefix="/api/scrape", tags=["scraping"])
app.include_router(waha.router, prefix="/webhook/waha", tags=["waha"])

@app.get("/")
def root():
    return {"ok": True, "name": settings.APP_NAME}

@app.websocket("/ws/conversations/{conversation_id}")
async def ws_conv(websocket: WebSocket, conversation_id: str):
    await manager.connect(conversation_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(conversation_id)
