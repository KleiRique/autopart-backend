from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.settings import settings
from app.routes import users, stores, conversations, scraping, waha

app = FastAPI(title=settings.APP_NAME)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.DEBUG else [settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas principais
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(stores.router, prefix="/api/stores", tags=["stores"])
app.include_router(conversations.router, prefix="/api/conversations", tags=["conversations"])
app.include_router(scraping.router, prefix="/api/scrape", tags=["scraping"])
app.include_router(waha.router, prefix="/webhook/waha", tags=["waha"])

@app.get("/")
def root():
    return {"ok": True, "name": settings.APP_NAME}

# WebSocket opcional (não interfere mais no deploy)
@app.websocket("/ws/conversations/{conversation_id}")
async def ws_conversation(websocket: WebSocket, conversation_id: str):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Mensagem recebida: {data}")
    except WebSocketDisconnect:
        print(f"Conexão encerrada: {conversation_id}")
