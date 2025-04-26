import requests

requisicao  = requests.get("https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL")

def cotacao_dolar():
    if requisicao.status_code == 200:
        
        cotacao = requisicao.json()
        dolar = cotacao['USDBRL']['bid']
        # print(f"Valor do Dólar: {dolar}")
        
        return dolar

    else:
        print("Erro ao acessar a API")
        return False