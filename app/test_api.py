import requests
import time

BASE_URL = "http://localhost:8000"

def print_section(title):
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}\n")

def test_api():
    """Testa todos os endpoints da API"""

    print_section("🧪 TESTE DA API LLM CHAT")

    # 1. Testar root
    print_section("1️⃣ Testando endpoint root")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.json()}")
    except Exception as e:
        print(f"❌ Erro: {e}")
        return

    # 2. Registrar usuário
    print_section("2️⃣ Registrando novo usuário")
    username = f"test_user_{int(time.time())}"
    password = "senha123"

    try:
        response = requests.post(f"{BASE_URL}/users/register", json={
            "username": username,
            "password": password
        })
        print(f"Status: {response.status_code}")
        print(f"Usuário criado: {response.json()}")
    except Exception as e:
        print(f"❌ Erro ao registrar: {e}")
        return

    # 3. Login
    print_section("3️⃣ Fazendo login")
    try:
        response = requests.post(f"{BASE_URL}/users/login", json={
            "username": username,
            "password": password
        })

        if response.status_code != 200:
            print(f"❌ Erro no login: {response.json()}")
            return

        data = response.json()
        token = data["access_token"]
        print(f"✅ Login realizado!")
        print(f"Token: {token[:50]}...")
        print(f"Usuário: {data['user']}")
    except Exception as e:
        print(f"❌ Erro ao fazer login: {e}")
        return

    # Headers com token
    headers = {"Authorization": f"Bearer {token}"}

    # 4. Testar /users/me
    print_section("4️⃣ Obtendo dados do usuário atual")
    try:
        response = requests.get(f"{BASE_URL}/users/me", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Dados: {response.json()}")
    except Exception as e:
        print(f"❌ Erro: {e}")

    # 5. Enviar mensagem ao chat
    print_section("5️⃣ Enviando mensagem ao LLM")
    try:
        response = requests.post(
            f"{BASE_URL}/chat/",
            headers=headers,
            json={"question": "Diga olá em 5 idiomas diferentes"}
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Mensagem enviada!")
            print(f"ID: {data['id']}")
            print(f"Pergunta: {data['question']}")
            print(f"Resposta: {data['answer'][:200]}...")
        else:
            print(f"❌ Erro: {response.json()}")
    except Exception as e:
        print(f"❌ Erro ao enviar mensagem: {e}")

    # 6. Enviar mais mensagens
    print_section("6️⃣ Enviando mais mensagens")
    questions = [
        "Qual é a capital do Brasil?",
        "Explique o que é FastAPI em uma frase",
        "Conte uma piada curta"
    ]

    for q in questions:
        try:
            response = requests.post(
                f"{BASE_URL}/chat/",
                headers=headers,
                json={"question": q}
            )
            if response.status_code == 200:
                print(f"✅ '{q[:40]}...'")
            time.sleep(0.5)  # Evita rate limit
        except Exception as e:
            print(f"❌ Erro: {e}")

    # 7. Ver histórico
    print_section("7️⃣ Recuperando histórico de conversas")
    try:
        response = requests.get(
            f"{BASE_URL}/chat/history?limit=10",
            headers=headers
        )

        if response.status_code == 200:
            messages = response.json()
            print(f"✅ Encontradas {len(messages)} mensagens no histórico:")
            for msg in messages[:3]:  # Mostra as 3 primeiras
                print(f"\n  📝 Pergunta: {msg['question'][:50]}...")
                print(f"  💬 Resposta: {msg['answer'][:80]}...")
                print(f"  🕐 Data: {msg['created_at']}")
        else:
            print(f"❌ Erro: {response.json()}")
    except Exception as e:
        print(f"❌ Erro ao buscar histórico: {e}")

    # 8. Testar autenticação inválida
    print_section("8️⃣ Testando token inválido")
    try:
        invalid_headers = {"Authorization": "Bearer token_invalido"}
        response = requests.get(f"{BASE_URL}/users/me", headers=invalid_headers)
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.json()}")
    except Exception as e:
        print(f"❌ Erro: {e}")

    print_section("🎉 TESTES CONCLUÍDOS!")

if __name__ == "__main__":
    test_api()
