from pydantic import BaseModel

class UserCreate(BaseModel):
    """Schema para criar/login de usuário"""
    username: str
    password: str

class UserRead(BaseModel):
    """Schema para ler dados do usuário"""
    id: int  # CORRIGIDO: era str, agora é int
    username: str

    class Config:
        from_attributes = True
