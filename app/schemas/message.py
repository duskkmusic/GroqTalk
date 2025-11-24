from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    """Schema para criar uma nova mensagem"""
    question: str

class MessageRead(BaseModel):
    """Schema para ler uma mensagem"""
    id: int
    user_id: int
    question: str
    answer: str
    created_at: datetime

    class Config:
        from_attributes = True
