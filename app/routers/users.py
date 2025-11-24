from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserRead
from app.services.auth_service import register_user, authenticate_user
from app.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Registra um novo usuário"""
    user = register_user(db, user_data.username, user_data.password)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome de usuário já existe"
        )

    return user

@router.post("/login")
def login(user_data: UserCreate, db: Session = Depends(get_db)):
    """Faz login e retorna token JWT"""
    auth_response = authenticate_user(db, user_data.username, user_data.password)

    if auth_response is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )

    return auth_response

@router.get("/me", response_model=UserRead)
def get_me(current_user = Depends(get_current_user)):
    """Retorna informações do usuário autenticado"""
    return current_user
