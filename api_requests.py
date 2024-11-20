import requests
import json

url = "https://statusinvest.com.br/category/advancedsearchresultpaginated"

querystring = {
    "search": '{"Sector":"","SubSector":"","Segment":"","my_range":"-1;1","forecast":{"upsidedownside":{"Item1":null,"Item2":null},"estimatesnumber":{"Item1":null,"Item2":null},"revisedup":true,"reviseddown":true,"consensus":[]},"dy":{"Item1":null,"Item2":null},"p_l":{"Item1":null,"Item2":null},"peg_ratio":{"Item1":null,"Item2":null},"p_vp":{"Item1":null,"Item2":null},"p_ativo":{"Item1":null,"Item2":null},"margembruta":{"Item1":null,"Item2":null},"margemebit":{"Item1":null,"Item2":null},"margemliquida":{"Item1":null,"Item2":null},"p_ebit":{"Item1":null,"Item2":null},"ev_ebit":{"Item1":null,"Item2":null},"dividaliquidaebit":{"Item1":null,"Item2":null},"dividaliquidapatrimonioliquido":{"Item1":null,"Item2":null},"p_sr":{"Item1":null,"Item2":null},"p_capitalgiro":{"Item1":null,"Item2":null},"p_ativocirculante":{"Item1":null,"Item2":null},"roe":{"Item1":null,"Item2":null},"roic":{"Item1":null,"Item2":null},"roa":{"Item1":null,"Item2":null},"liquidezcorrente":{"Item1":null,"Item2":null},"pl_ativo":{"Item1":null,"Item2":null},"passivo_ativo":{"Item1":null,"Item2":null},"giroativos":{"Item1":null,"Item2":null},"receitas_cagr5":{"Item1":null,"Item2":null},"lucros_cagr5":{"Item1":null,"Item2":null},"liquidezmediadiaria":{"Item1":null,"Item2":null},"vpa":{"Item1":null,"Item2":null},"lpa":{"Item1":null,"Item2":null},"valormercado":{"Item1":null,"Item2":null}}',
    "orderColumn": "",
    "isAsc": "",
    "page": "0",
    "take": "100",
    "CategoryType": "1",
}

headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "referer": "https://statusinvest.com.br/acoes/busca-avancada",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/113.0.0.0 (Edition std-1)",
    "x-requested-with": "XMLHttpRequest",
}

response = requests.get(url, headers=headers, params=querystring)

if response.status_code == 200:
    data = response.json()

    resultado_formatado = []

    for item in data["list"]:
        empresa = {
            "companyname": item.get("companyname"),
            "ticker": item.get("ticker"),
            "price": item.get("price"),
            "margembruta": item.get("margembruta"),
            "margemliquida": item.get("margemliquida"),
            "valordemercado": item.get("valormercado"),
            "segmentname": item.get("segmentname"),
        }
        resultado_formatado.append(empresa)

    with open("Json/empresas.json", "w", encoding="utf-8") as json_file:
        json.dump(resultado_formatado, json_file, ensure_ascii=False, indent=4)

    print("Arquivo JSON salvo com sucesso.")

else:
    print(f"Erro na requisição: {response.status_code}")
