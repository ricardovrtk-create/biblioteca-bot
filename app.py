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
    try:
        data = request.json
        mensagem = data.get("message", "")

        prompt = f"""
        Você é o assistente virtual da Biblioteca do IME-USP.
        Responda apenas perguntas relacionadas à biblioteca.
        Pergunta: {mensagem}
        """

        response = requests.post(
            "https://api.openai.com/v1/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4",
                "prompt": prompt,
                "max_tokens": 100
            }
        )

        # Verifique se a resposta foi bem-sucedida
        if response.status_code != 200:
            return jsonify({"error": f"Erro na API da OpenAI: {response.text}"}), 500

        # Tente acessar o campo "choices" de maneira segura
        response_data = response.json()
        if "choices" not in response_data:
            return jsonify({"error": "Resposta inesperada da OpenAI: 'choices' não encontrado"}), 500

        resposta_texto = response_data["choices"][0]["text"]
        
        return jsonify({"text": resposta_texto})
    
    except Exception as e:
        return jsonify({"error": f"Erro no servidor: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
