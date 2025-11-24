import bcrypt
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.user_repository import get_user_by_username, create_user
from app.dependencies import create_access_token

def hash_password(password: str) -> str:
    """Gera hash da senha usando bcrypt"""
    # Converte para bytes e gera hash
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha corresponde ao hash"""
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def register_user(db: Session, username: str, password: str):
    """Registra um novo usuário"""
    # Verifica se usuário já existe
    existing_user = get_user_by_username(db, username)
    if existing_user:
        return None

    # Cria novo usuário com senha hasheada
    hashed_password = hash_password(password)
    new_user = User(
        username=username,
        password_hash=hashed_password
    )

    return create_user(db, new_user)

def authenticate_user(db: Session, username: str, password: str):
    """Autentica usuário e retorna token JWT"""
    user = get_user_by_username(db, username)

    # Verifica se usuário existe e senha está correta
    if not user or not verify_password(password, user.password_hash):
        return None

    # Gera token JWT
    access_token = create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username
        }
    }
