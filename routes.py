from flask import jsonify, request, render_template
from openai import OpenAI
from dotenv import load_dotenv
from os import getenv
import json
from api import app

MEMORIA = "Json/memoria_openai.json"
EMPRESA_JSON = "Json/empresas.json"

def carregar_json_empresas(data):
    with open(data, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)
    return []


dados_empresas = carregar_json_empresas(EMPRESA_JSON)


def carregar_memoria_api():
    try:
        with open(MEMORIA, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return {"historico": []}


def salvar_memoria_api(historico):
    with open(MEMORIA, "w", encoding="utf-8") as arquivo:
        json.dump({"historico": historico}, arquivo, ensure_ascii=False, indent=4)


def criacao_prompt(pergunta_usuario):
    memoria = carregar_memoria_api()
    historico = memoria.get("historico", [])

    prompt = ""

    for interacao in historico:
        prompt += f"Usuário: {interacao['mensagem']}\nIA: {interacao['resposta']}\n"

    prompt += "\nInformação de algumas EMPRESAS de um JSON que o código leu, quero que você responda minhas perguntas com base nesses dados, quando perguntar algo muito especificio, se baseie nessas informações:\n\n"
    for empresa in dados_empresas:
        prompt += f"( Nome: {empresa['companyname']}, Ticker: {empresa['ticker']}, Preço: {empresa['price']}, Margem Bruta: {empresa['margembruta']}, Margem Líquida: {empresa['margemliquida']}, Valor de Mercado: {empresa['valordemercado']}, Segmento: {empresa['segmentname']} )\n"

    prompt += f"Usuário: {pergunta_usuario}\nIA:"

    return prompt


def processamento_resposta(data):
    load_dotenv()
    API_KEY_OPENAI = getenv("OPENAI_API_KEY")

    OPENAI = OpenAI(api_key=API_KEY_OPENAI)

    prompt = f"Aqui é formatação da mensagem a ser exibida, só retorne a mensagem formatada em html com a estilização, então caso de seja possivel fazer uma tabela retorne tabela com parametro style='table_color', retorne texto como parametro style='bot-text', é preciso que você só retorne o html mesmo, sem mensagem a mais.\n\n"
    prompt += data

    response = OPENAI.chat.completions.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}],
    )

    texto = response.choices[0].message.content.strip()

    return texto


def api_openai(data):
    load_dotenv()
    
    API_KEY_OPENAI = getenv("OPENAI_API_KEY")

    OPENAI = OpenAI(api_key=API_KEY_OPENAI)

    prompt = criacao_prompt(data)

    print(prompt)
    response = OPENAI.chat.completions.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}],
    )

    texto = response.choices[0].message.content.strip()

    texto_formatado = processamento_resposta(texto)

    historico = carregar_memoria_api().get("historico", [])
    historico.append({"mensagem": data, "resposta": texto_formatado})
    salvar_memoria_api(historico)


    return {"resposta": texto_formatado}

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/openai", methods=["POST"])
def api():
    data = request.get_json()
    pergunta = data["user"]
    resposta = api_openai(data=pergunta)

    return jsonify(resposta)


@app.route("/chat", methods=["GET"])
def carregar_chat():
    chat = carregar_memoria_api()
    historico = chat.get("historico", [])
    return jsonify(historico)
