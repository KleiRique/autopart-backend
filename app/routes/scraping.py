from fastapi import APIRouter
from app.web_scraper import scrape_store_page
router = APIRouter()
@router.post("/store")
async def scrape_store(url: str):
    return await scrape_store_page(url)
