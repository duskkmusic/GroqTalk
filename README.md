🤖 LLM Chat API com FastAPI
API de chat com LLM usando Groq, autenticação JWT e PostgreSQL.
📋 Pré-requisitos

Python 3.9+
PostgreSQL
Conta Groq (API Key gratuita)

🚀 Instalação
1. Clone e configure o ambiente
bash# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas credenciais
2. Configure o banco de dados
Certifique-se que o PostgreSQL está rodando e crie o banco:
sqlCREATE DATABASE llm_chat_db;
3. Execute as migrações
bash# As tabelas serão criadas automaticamente ao iniciar
python main.py
4. (Opcional) Popule com dados de teste
bashpython seeds.py
🏃 Como Usar
Iniciar o servidor
bashuvicorn app.main:app --reload --host 0.0.0.0 --port 8000
Acesse a documentação interativa: http://localhost:8000/docs
🔐 Endpoints de Autenticação
1. Registrar novo usuário
bashPOST /users/register
Content-Type: application/json

{
  "username": "seu_usuario",
  "password": "sua_senha"
}
Resposta:
json{
  "id": 1,
  "username": "seu_usuario"
}
2. Fazer login
bashPOST /users/login
Content-Type: application/json

{
  "username": "seu_usuario",
  "password": "sua_senha"
}
Resposta:
json{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "seu_usuario"
  }
}
3. Obter dados do usuário atual
bashGET /users/me
Authorization: Bearer {seu_token}
💬 Endpoints de Chat
1. Enviar mensagem ao LLM
bashPOST /chat/
Authorization: Bearer {seu_token}
Content-Type: application/json

{
  "question": "O que é FastAPI?"
}
Resposta:
json{
  "id": 1,
  "user_id": 1,
  "question": "O que é FastAPI?",
  "answer": "FastAPI é um framework web moderno...",
  "created_at": "2024-01-15T10:30:00Z"
}
2. Ver histórico de conversas
bashGET /chat/history?limit=10&offset=0
Authorization: Bearer {seu_token}
🔧 Exemplo com cURL
bash# 1. Registrar
curl -X POST "http://localhost:8000/users/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"teste","password":"teste123"}'

# 2. Login
TOKEN=$(curl -X POST "http://localhost:8000/users/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"teste","password":"teste123"}' | jq -r '.access_token')

# 3. Enviar mensagem
curl -X POST "http://localhost:8000/chat/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question":"Explique machine learning"}'

# 4. Ver histórico
curl -X GET "http://localhost:8000/chat/history" \
  -H "Authorization: Bearer $TOKEN"
🐍 Exemplo com Python
pythonimport requests

BASE_URL = "http://localhost:8000"

# 1. Registrar usuário
response = requests.post(f"{BASE_URL}/users/register", json={
    "username": "python_user",
    "password": "senha123"
})
print(response.json())

# 2. Fazer login
response = requests.post(f"{BASE_URL}/users/login", json={
    "username": "python_user",
    "password": "senha123"
})
token = response.json()["access_token"]

# 3. Headers com autenticação
headers = {"Authorization": f"Bearer {token}"}

# 4. Enviar mensagem
response = requests.post(
    f"{BASE_URL}/chat/",
    headers=headers,
    json={"question": "O que é inteligência artificial?"}
)
print(response.json())

# 5. Ver histórico
response = requests.get(f"{BASE_URL}/chat/history", headers=headers)
print(response.json())
📊 Estrutura do Projeto
my-llm-api/
├── app/
│   ├── models/           # Modelos SQLAlchemy
│   ├── repositories/     # Camada de acesso a dados
│   ├── routers/          # Endpoints da API
│   ├── schemas/          # Schemas Pydantic
│   ├── services/         # Lógica de negócio
│   ├── database.py       # Configuração do banco
│   └── dependencies.py   # Dependências (auth)
├── .env                  # Variáveis de ambiente
├── main.py              # Aplicação principal
├── seeds.py             # Dados de teste
└── requirements.txt     # Dependências Python
🔒 Segurança

✅ Senhas hasheadas com bcrypt
✅ JWT para autenticação stateless
✅ Tokens expiram em 24 horas
✅ Proteção de rotas sensíveis
⚠️ Mude a SECRET_KEY em produção!

🐛 Resolução de Problemas
Erro de conexão com banco
bash# Verifique se PostgreSQL está rodando
sudo systemctl status postgresql

# Teste a conexão
psql -U seu_usuario -d llm_chat_db
Token inválido

Certifique-se de incluir "Bearer " antes do token
Verifique se o token não expirou (24h)
Faça login novamente para obter novo token

Groq API Key inválida

Obtenha uma chave em: https://console.groq.com
Configure no arquivo .env

📝 Notas

O histórico de chat está ordenado por data (mais recente primeiro)
Cada usuário vê apenas suas próprias mensagens
Usuários podem ter o mesmo nome de conversa
O modelo padrão é llama-3.1-8b-instant (rápido e gratuito)

🤝 Contribuindo
Sinta-se à vontade para abrir issues ou pull requests!
