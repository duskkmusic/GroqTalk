from app.database import SessionFactory
from app.services.auth_service import register_user
from dotenv import load_dotenv

load_dotenv()

def seed_database():
    """Popula banco de dados com dados de teste"""
    db = SessionFactory()

    try:
        print("🌱 Iniciando seeds...")

        # Cria usuários de teste
        users_data = [
            {"username": "admin", "password": "admin123"},
            {"username": "teste", "password": "teste123"},
            {"username": "demo", "password": "demo123"}
        ]

        for user_data in users_data:
            user = register_user(db, user_data["username"], user_data["password"])
            if user:
                print(f"✅ Usuário '{user.username}' criado com sucesso!")
            else:
                print(f"⚠️  Usuário '{user_data['username']}' já existe")

        print("\n🎉 Seeds concluídas!")

    except Exception as e:
        print(f"❌ Erro ao executar seeds: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
