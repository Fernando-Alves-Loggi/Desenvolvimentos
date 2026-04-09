import requests
import pandas as pd
import logging
import os
import time
from datetime import datetime
from dotenv import load_dotenv

# =========================
# CARREGAR VARIÁVEIS
# =========================

load_dotenv()

API_URL = "https://managersaas.tecnospeed.com.br:8081/ManagerAPIWeb/nfe/envia"

# GRUPO = os.getenv("GRUPO")
# CNPJ = os.getenv("CNPJ")
# USER = os.getenv("API_USER")
# PASSWORD = os.getenv("API_PASSWORD")

GRUPO = "PLUG_24217653000195"
CNPJ = "24217653000195"
USER = "admin"
PASSWORD = "D3A8475D2B0A5BE8017DBF9F6C812707"

PLANILHA = "C:\\Users\\fernando.araujo_logg\\Downloads\\layout_mde.xlsx"

# =========================
# CONFIGURAR LOG
# =========================

if not os.path.exists("logs"):
    os.makedirs("logs")

log_file = f"logs/manifestacao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logging.info("==== INICIANDO PROCESSO DE MANIFESTAÇÃO ====")
logging.info(f"Grupo: {GRUPO}")
logging.info(f"CNPJ: {CNPJ}")

# =========================
# FUNÇÃO MANIFESTAR
# =========================

def manifestar_nota(chave, tipoevento, justificativa):

    data_evento = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    linhas = [
        "DOCUMENTO=MDE",
        f"TIPOEVENTO={tipoevento}",
        f"CHAVENOTA={chave}",
        f"DHEVENTO={data_evento}",
        "FUSO=-03:00",
        f"JUSTIFICATIVA={justificativa}"
    ]

    arquivo = "\r\n".join(linhas)

    payload = {
        "encode": "true",
        "grupo": GRUPO,
        "cnpj": CNPJ,
        "arquivo": arquivo
    }

    try:

        logging.info(f"Enviando manifestação | CHAVE={chave} | EVENTO={tipoevento}")

        logging.info("Conteúdo enviado no campo 'arquivo':")

        response = requests.post(
            API_URL,
            auth=(USER, PASSWORD),
            data=payload,
            timeout=180
        )

        logging.info(f"Status HTTP: {response.status_code}")
        logging.info(f"Resposta API: {response.text}")

        return response.status_code, response.text

    except Exception as e:

        logging.error(f"Erro ao manifestar nota {chave}")
        logging.exception(e)

        return None, str(e)

# =========================
# LER PLANILHA
# =========================

try:

    df = pd.read_excel(PLANILHA, dtype=str)

    logging.info(f"{len(df)} notas encontradas na planilha")

except Exception as e:

    logging.error("Erro ao ler planilha")
    logging.exception(e)
    raise SystemExit()

# =========================
# PROCESSAR NOTAS
# =========================

resultados = []

for index, row in df.iterrows():

    try:

        chave = str(row["chave_nota"]).strip()
        tipoevento = int(row["tipo_evento"])
        justificativa = str(row["Justificativa"]).strip()

        logging.info(f"Processando {index+1}/{len(df)}")

        status, retorno = manifestar_nota(chave, tipoevento, justificativa)

        resultados.append({
            "chavenota": chave,
            "tipoevento": tipoevento,
            "status_http": status,
            "retorno_api": retorno
        })

        # evita sobrecarga na API
        time.sleep(1)

    except Exception as e:

        logging.error(f"Erro ao processar linha {index}")
        logging.exception(e)

# =========================
# SALVAR RESULTADOS
# =========================

df_result = pd.DataFrame(resultados)

arquivo_saida = f"resultado_manifestacao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

df_result.to_excel(arquivo_saida, index=False)

logging.info("Arquivo de resultado salvo: " + arquivo_saida)

logging.info("==== PROCESSO FINALIZADO ====")