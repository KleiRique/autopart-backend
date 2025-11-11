from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class UserCreate(BaseModel):
    email: str
    password: str
    name: str

class UserOut(BaseModel):
    id: int
    email: str
    name: str
    model_config = ConfigDict(from_attributes=True)

class StoreCreate(BaseModel):
    name: str
    whatsapp_number: str
    base_url: Optional[str] = None

class StoreOut(StoreCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ConversationCreate(BaseModel):
    part_query: str
    store_ids: List[int]

class MessageIn(BaseModel):
    content: str

class MessageOut(BaseModel):
    id: int
    role: str
    store_id: Optional[int] = None
    content: str
    model_config = ConfigDict(from_attributes=True)

class QuoteOut(BaseModel):
    id: int
    store_id: int
    price: float
    delivery_days: int
    notes: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
