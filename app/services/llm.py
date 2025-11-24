import os
from groq import Groq

def get_groq_client():
    """
    Cria o cliente Groq de forma segura.
    Suporta proxies via variáveis de ambiente HTTP_PROXY e HTTPS_PROXY.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY não encontrada no .env")

    # Configura proxies via variáveis de ambiente (opcional)
    proxies = {}
    http_proxy = os.getenv("HTTP_PROXY")
    https_proxy = os.getenv("HTTPS_PROXY")
    if http_proxy:
        proxies["http"] = http_proxy
    if https_proxy:
        proxies["https"] = https_proxy

    # Cria o cliente
    client_kwargs = {"api_key": api_key}
    if proxies:
        client_kwargs["proxies"] = proxies  # só adiciona se houver proxies configurados

    return Groq(**client_kwargs)


def ask_llm(prompt: str) -> str:
    """
    Envia pergunta ao LLM e retorna a resposta.
    Retorna mensagem de erro amigável caso falhe.
    """
    try:
        client = get_groq_client()
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )
        # Retorna o conteúdo da primeira escolha
        return response.choices[0].message.content

    except Exception as e:
        # Loga o erro no console para debug
        print(f"[LLM ERROR] {str(e)}")
        return f"Erro ao consultar LLM: {str(e)}"
