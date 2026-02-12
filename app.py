from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "Bot Biblioteca rodando!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    mensagem = data.get("message", "")

    prompt = f"""
Você é o assistente virtual da Biblioteca do IME-USP.

Responda apenas perguntas relacionadas à biblioteca.
Se não souber ou não for sobre a biblioteca, diga que não possui essa informação.

Informações oficiais:
- Horário: segunda a sexta, das 8h às 18h.
- Empréstimo: apenas para usuários com vínculo ativo com a USP.
- Renovação: feita pelo sistema institucional.
- Usuários externos: apenas consulta local.

Pergunta:
{mensagem}
"""

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2
        }
    )

    resposta_texto = response.json()["choices"][0]["message"]["content"]

    return jsonify({"text": resposta_texto})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
