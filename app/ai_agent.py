from typing import Iterable, List, Dict, Optional
from app.redis_client import cache_setex
from app.waha_client import send_whatsapp_text

PROMPT = "Você é um assistente de cotações para autopeças. Responda no formato: PRECO=123.45; PRAZO=2; OBS=..."

async def fanout_request(part_query: str, conv_id: int, stores: Iterable[dict]):
    for s in stores:
        body = (f"[Cotação Automática]\nPedido: {part_query}\n"
                f"Responda no formato: PRECO=123.45; PRAZO=2; OBS=...")
        await send_whatsapp_text(s["whatsapp_number"], body)
    cache_setex(f"conv:{conv_id}:status", "awaiting_store_quotes", 3600)

def parse_store_reply(text: str) -> Optional[dict]:
    try:
        parts = dict((kv.split("=")[0].strip().lower(), kv.split("=")[1].strip()) for kv in text.split(";"))
        price = float(parts.get("preco") or parts.get("preço"))
        days = int(parts.get("prazo"))
        notes = parts.get("obs")
        return {"price": price, "delivery_days": days, "notes": notes}
    except Exception:
        return None

async def decide_best_quote(quotes: List[Dict]) -> Optional[Dict]:
    if not quotes: return None
    return sorted(quotes, key=lambda q: (q["price"], q["delivery_days"]))[0]
