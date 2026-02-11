import requests
from time import sleep as slp
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import pandas as pd

#Ler planilha
df = pd.read_excel("/home/fernando-araujo/Documentos/Desenvolvimentos/SAP/Items.xlsx", dtype=str)

#Carregar variáveis de ambiente
load_dotenv()

#URL da API
url = "https://loggi-dev-qa.it-cpi003-rt.cfapps.us10.hana.ondemand.com/http/s4/api/accounting"

#Credenciais
username = os.getenv("API_USERNAME")
password = os.getenv("API_PASSWORD")

#Iterar linha a linha da planilha
for index, row in df.iterrows():

  payload = {
    "document_type": row["Tipo Documento"],
    "period_start": "2026-02-01T00:00:00",
    "period_end": "2026-02-27T00:00:00",
    "company_code": "L4B",
    "amount": row["Invoice amount"],
    "bp_number": row["Numero BP"],
    "loggi_id": row["Loggi ID"],
    "purchase_order_number": "4600033295",
    "document_date": row["Data de emissão"],
    "due_date": row["Data de emissão"],
    "loggi_transaction_id": 2345
  }

  #Enviar requisição POST
  response = requests.get(
    url,
    json=payload,
    auth=HTTPBasicAuth(username, password),
    timeout=30
    )

  with open("response_log.txt", "a") as log_file:
    log_file.write(f"Resposta da API: {response.text}\n")

  print("Resposta da API:", response.text, response.status_code)

  slp(1)
