from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.settings import settings
from app.routes import users, stores, conversations, scraping, waha
from app.ws import ws_conversation_handler

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

# Rota de teste
@app.get("/")
def root():
    return {"ok": True, "name": settings.APP_NAME}

# WebSocket para conversas em tempo real
@app.websocket("/ws/conversations/{conversation_id}")
async def ws_conv(websocket: WebSocket, conversation_id: str):
    await ws_conversation_handler(websocket, conversation_id)
