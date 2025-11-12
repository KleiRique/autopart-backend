from fastapi import APIRouter, Depends
from app.schemas import WahaMessage
from app.ai_agent import process_message

router = APIRouter(prefix="/waha", tags=["WAHA"])

@router.post("/webhook")
async def waha_webhook(payload: dict):
    # Recebe mensagens do WAHA (WhatsApp API)
    # e envia para o agente de IA processar.
    message = WahaMessage(
        sender=payload.get("from"),
        text=payload.get("text", {}).get("body", "")
    )

    response = await process_message(message.sender, message.text)

    return {
        "reply": response
    }
