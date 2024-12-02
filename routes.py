# app/api.py
from app import app
from flask import jsonify, request, render_template
from openai import OpenAI
from dotenv import load_dotenv
from os import getenv
import json
import os

# Carregar variáveis de ambiente
load_dotenv()

# Configuração de caminhos para os arquivos JSON
MEMORIA = "Json/memoria_openai.json"
EMPRESA_JSON = "Json/empresas.json"

# Função para carregar dados das empresas
def carregar_json_empresas(data):
    if not os.path.exists(data):
        print(f"Erro: o arquivo {data} não existe.")
        return []
    with open(data, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)
    return []


# Carregar os dados das empresas
dados_empresas = carregar_json_empresas(EMPRESA_JSON)

# Funções de memória
def carregar_memoria_api():
    try:
        with open(MEMORIA, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return {"historico": []}

def salvar_memoria_api(historico):
    with open(MEMORIA, "w", encoding="utf-8") as arquivo:
        json.dump({"historico": historico}, arquivo, ensure_ascii=False, indent=4)

# Funções para criação do prompt e resposta da API OpenAI
def criacao_prompt(pergunta_usuario):
    memoria = carregar_memoria_api()
    historico = memoria.get("historico", [])
    prompt = ""
    for interacao in historico:
        prompt += f"Usuário: {interacao['mensagem']}\nIA: {interacao['resposta']}\n"
    prompt += "\nInformação de algumas EMPRESAS de um JSON que o código leu, quero que você responda minhas perguntas com base nesses dados:\n\n"
    for empresa in dados_empresas:
        prompt += f"( Nome: {empresa['companyname']}, Ticker: {empresa['ticker']}, Preço: {empresa['price']}, Margem Bruta: {empresa['margembruta']}, Margem Líquida: {empresa['margemliquida']}, Valor de Mercado: {empresa['valordemercado']}, Segmento: {empresa['segmentname']} )\n"
    prompt += f"Usuário: {pergunta_usuario}\nIA:"
    return prompt

def processamento_resposta(data):
    API_KEY_OPENAI = getenv("OPENAI_API_KEY")
    try:
        OPENAI = OpenAI(api_key=API_KEY_OPENAI)
        prompt = f"Aqui é formatação da mensagem a ser exibida, só retorne a mensagem formatada em html com a estilização...\n\n"
        prompt += data
        response = OPENAI.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        texto = response.choices[0].message.content.strip()
        return texto
    except Exception as e:
        print(f"Erro ao processar a resposta: {e}")
        return "Ocorreu um erro ao processar a resposta da IA."

def api_openai(data):
    try:
        prompt = criacao_prompt(data)
        response = OpenAI(api_key=getenv("OPENAI_API_KEY")).chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        texto = response.choices[0].message.content.strip()
        texto_formatado = processamento_resposta(texto)
        historico = carregar_memoria_api().get("historico", [])
        historico.append({"mensagem": data, "resposta": texto_formatado})
        salvar_memoria_api(historico)
        return {"resposta": texto_formatado}
    except Exception as e:
        print(f"Erro ao processar a requisição: {e}")
        return {"error": "Ocorreu um erro no processamento da solicitação."}

# Definindo as rotas
@app.route("/")
def index():
    return render_template("help.html")

@app.route("/talk")
def talk():
    return render_template("index.html")

@app.route("/openai", methods=["POST"])
def api():
    try:
        data = request.get_json()
        pergunta = data["user"]
        resposta = api_openai(data=pergunta)
        return jsonify(resposta)
    except Exception as e:
        print(f"Erro no endpoint /openai: {e}")
        return jsonify({"error": "Erro ao processar a requisição."})

@app.route("/chat", methods=["GET"])
def carregar_chat():
    try:
        chat = carregar_memoria_api()
        historico = chat.get("historico", [])
        return jsonify(historico)
    except Exception as e:
        print(f"Erro ao carregar o chat: {e}")
        return jsonify({"error": "Erro ao carregar o histórico."})