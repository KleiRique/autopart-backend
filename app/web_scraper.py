import httpx
from bs4 import BeautifulSoup

async def scrape_store_page(url: str) -> dict:
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url); r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        return {'title': soup.title.text.strip() if soup.title else None}
