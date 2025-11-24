from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.message import Message
from app.schemas.message import MessageRead, MessageCreate
from app.services.llm import ask_llm
from app.dependencies import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.get("/history", response_model=list[MessageRead])
def history(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Retorna histórico de mensagens do usuário atual"""
    return db.query(Message)\
        .filter(Message.user_id == current_user.id)\
        .order_by(Message.created_at.desc())\
        .offset(offset)\
        .limit(limit).all()

@router.post("/", response_model=MessageRead)
def chat(
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Envia uma mensagem ao LLM e salva no histórico"""
    # Obtém resposta do LLM
    answer = ask_llm(message_data.question)

    # Cria mensagem associada ao usuário atual
    message = Message(
        user_id=current_user.id,  # CORRIGIDO: associa ao usuário
        question=message_data.question,
        answer=answer
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message
