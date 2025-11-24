from fastapi import FastAPI
from dotenv import load_dotenv

# Carrega variáveis de ambiente ANTES de importar routers
load_dotenv()

from app.routers import chat, users
from app.database import create_tables

app = FastAPI(
    title="LLM Chat API",
    description="API de chat com LLM usando Groq e autenticação JWT",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    """Cria tabelas no banco ao iniciar"""
    create_tables()

# Inclui routers
app.include_router(users.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {
        "message": "API com Groq online!",
        "docs": "/docs",
        "endpoints": {
            "register": "POST /users/register",
            "login": "POST /users/login",
            "me": "GET /users/me",
            "chat": "POST /chat/",
            "history": "GET /chat/history"
        }
    }
