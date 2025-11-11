import httpx
from app.settings import settings
async def send_whatsapp_text(to_number: str, text: str):
    url = f"{settings.WAHA_BASE_URL}/api/sendText"
    payload = {
        "chatId": to_number if to_number.endswith("@c.us") else f"{to_number}@c.us",
        "text": text,
        "session": settings.WAHA_DEFAULT_SENDER,
        "token": settings.WAHA_TOKEN,
    }
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.post(url, json=payload)
        r.raise_for_status()
        return r.json()
