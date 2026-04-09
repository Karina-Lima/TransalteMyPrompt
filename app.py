from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = Flask(__name__)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/optimize", methods=["POST"])
def optimize():

    try:
        data = request.get_json()
        user_prompt = data.get("prompt")

        if not user_prompt:
            return jsonify({"error": "Prompt vazio"}), 400

        response = client.models.generate_content(
            model="models/gemini-2.5-flash-lite",
            contents=f"""
Você é um especialista sênior em Prompt Engineering.

Sua tarefa é transformar prompts simples em prompts otimizados para IA.

Você deve:
- entender intenção do usuário;
- adicionar contexto;
- estruturar melhor;
- aumentar clareza;
- melhorar definição de tarefa.

NÃO apenas reescreva:
realmente aprimore a engenharia do prompt.

O score deve seguir esta lógica:
- Prompt ruim porém funcional: 40–60
- Prompt razoável: 60–80
- Prompt excelente: 80–100
- Evite notas extremamente baixas salvo casos inutilizáveis.

RETORNE SOMENTE JSON.

Formato:

{{
    "optimized_prompt": "prompt melhorado",
    "score": 0,
    "strengths": ["item 1", "item 2"],
    "improvements": ["item 1", "item 2"]
}}

Prompt original:
{user_prompt}
"""
        )

        cleaned_response = (
            response.text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        print("RESPOSTA IA:")
        print(cleaned_response)

        try:
            result = json.loads(cleaned_response)

        except Exception:
            result = {
                "optimized_prompt": cleaned_response,
                "score": 85,
                "strengths": [
                    "Boa estrutura geral"
                ],
                "improvements": [
                    "Adicionar mais contexto"
                ]
            }

        return jsonify(result)

    except Exception as e:
        print("ERRO BACKEND:")
        print(str(e))

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)