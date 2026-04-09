import requests

# Configurações da API
url = "https://managersaas.tecnospeed.com.br:8081/ManagerAPIWeb/mdfe/consulta"

# Headers: Requer autenticação Basic [cite: 22, 23]
# Substitua pelo seu usuário:senha codificados em Base64
headers = {
    "Authorization": "Basic YWRtaW46RDNBODQ3NUQyQjBBNUJFODAxN0RCRjlGNkM4MTI3MDc==" 
}

# Parâmetros da Querystring [cite: 24, 25]
params = {
    "Grupo": "PLUG_24217653000195",        # Nome do grupo no SaaS [cite: 26, 27]
    "CNPJ": "24217653004263",            # Apenas números [cite: 28, 29]
    "Filtro": "chave = 35240607337935000107550010004909171842596948",   # Exemplo de filtro [cite: 30, 31]
    "Campos": "chave,situacao,numero",   # Campos que deseja retornar [cite: 32, 33]
    "Limite": 1,                        # Máximo de 100 registros [cite: 34, 35, 36]
    "Ordem": "dtemissao desc",           # Ordenação decrescente [cite: 37, 38, 39]
    "Visao": "TspdMDFeVWConsulta"        # Tabela da consulta [cite: 40, 41]
}

try:
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        # O retorno virá conforme a ordem informada no parâmetro 'Campos' [cite: 48]
        print("Resultado da Consulta:")
        print(response.text)
    else:
        print(f"Erro na consulta. Status Code: {response.status_code}")
        print(f"Detalhes: {response.text}")

except Exception as e:
    print(f"Ocorreu um erro na requisição: {e}")