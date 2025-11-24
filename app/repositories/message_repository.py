from sqlalchemy.orm import Session
from app.models.message import Message

def create_message(db: Session, message: Message):
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

def get_user_message(db: Session, user_id: int, limit: int = 10, offset: int = 0):
    return db.query(Message).filter(Message.user_id == user_id)\
        .limit(limit).offset(offset).all()
