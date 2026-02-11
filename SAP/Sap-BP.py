import requests
from time import sleep as slp
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import pandas as pd

#Ler planilha
df = pd.read_excel("/home/fernando-araujo/Documentos/Desenvolvimentos/SAP/base_cadastros.xlsx", dtype=str)

#Carregar variáveis de ambiente
load_dotenv()

#URL da API
# url = "https://loggi-dev-qa.it-cpi003-rt.cfapps.us10.hana.ondemand.com/http/s4/api/BusinessPartner"
url = "https://loggi-prod.it-cpi008-rt.cfapps.br10.hana.ondemand.com/http/s4/api/BusinessPartner"

#Credenciais
username = os.getenv("API_USERNAME")
password = os.getenv("API_PASSWORD")

#Iterar linha a linha da planilha
for index, row in df.iterrows():
  identificacao = "" if pd.isna(row["CNPJ/CPF"]) else str(row["CNPJ/CPF"]).strip()

  if len(identificacao) == 14:
    payload = {
      "BusinessPartnerGrouping": "BP02",
      "IsNaturalPerson": "",
      "OrganizationBPName1": row["NOME EMPRESARIAL"],
      "OrganizationBPName2": "",
      "SearchTerm1": row["NOME EMPRESARIAL"],
      "SearchTerm2": row["CNPJ/CPF"],
      "BusinessPartnerType": "0014",

      "to_BusinessPartnerTax": [
          {
            "BPTaxType": "BR1",
            "BPTaxNumber": row["CNPJ/CPF"]
          },
          {
            "BPTaxType": "BR3",
            "BPTaxNumber": "ISENTO"
          }],
      "to_BusinessPartnerAddress": {
            "StreetName": row["LOGRADOURO"],                                                                      
            "HouseNumber": row["NÚMERO"],
            "District": row["BAIRRO/DISTRITO"],
            "PostalCode": row["CEP"],
            "CityName": row["MUNICÍPIO"],
            "Country": "BR",
            "Region": row["UF"],
            "Language": "PT",
            "to_EmailAddress": [
              {
                "EmailAddress": ""
              }
            ],
            "to_PhoneNumber": [
              {
                "DestinationLocationCountry": "BR",
                "PhoneNumber": ""
              }
            ]
          },
            "to_PhoneNumber":[
                {
                  "PhoneNumber": "",
                  "IsDefaultPhoneNumber": "false"
                }
              ],
      "to_Supplier": {
        "to_SupplierCompany": [
            {
              "CompanyCode": "LL4B",
              "ReconciliationAccount": "211001",
              "PaymentTerms": "NT00",
              "PaymentMethodsList": "NISTYZMJLV",
              "SupplierAccountGroup": "SUPL",
              "IsToBeCheckedForDuplicates": "true",
              "to_SupplierWithHoldingTax": []
            },
            {
              "CompanyCode": "LTEC",
              "ReconciliationAccount": "211001",
              "PaymentTerms": "NT00",
              "PaymentMethodsList": "NISTYZMJLV",
              "SupplierAccountGroup": "SUPL",
              "IsToBeCheckedForDuplicates": "true",
              "to_SupplierWithHoldingTax": []
            }
          ]
        },
        "to_SupplierPurchasingOrg": [
              {
                "PurchasingOrganization": "OC01",
                "PurchasingGroup": "",
                "PaymentTerms": "NT00",
                "PurchaseOrderCurrency": "BRL",
                "CalculationSchemaGroupCode": "R2",
                "InvoiceIsGoodsReceiptBased": "true",
                "InvoiceIsServiceBased": "true",
                "PurOrdAutoGenerationIsAllowed": "true",
                "DeletionIndicator": "false",
                "PurchasingIsBlockedForSupplier": "false",
                "to_PartnerFunction": [
                  {
                    "PartnerFunction": "EP",
                    "ReferenceSupplier": ""
                  },
                  {
                    "PartnerFunction": "FN",
                    "ReferenceSupplier": ""
                  },
                  {
                    "PartnerFunction": "EF",
                    "ReferenceSupplier": ""
                  }
                ]
              }
            ],
        "to_BusinessPartnerBank": [
          {
            "BankCountryKey": "BR",
            "BankNumber": row["CODIGO BANCO"],
            "bank_agency": row["AGENCIA"],
            "BankAccount": row["CONTA"],
            "BankControlKey": row["DIGITO CONTA"],
            "BankAccountName": row["NOME DO BANCO"]
        }
      ]  
  }
 
  elif len(identificacao) <= 11:
    payload = {
    "BusinessPartnerGrouping": "BP02",
    "IsNaturalPerson": "X",
    "OrganizationBPName1": row["Nome Pessoa Fisica"],
    "OrganizationBPName2": row["Sobrenome Pessoa Fisica"],
    "SearchTerm1": row["Nome Pessoa Fisica"],
    "SearchTerm2": row["CNPJ/CPF"],
    "BusinessPartnerType": "0014",

    "to_BusinessPartnerTax": [
        {
          "BPTaxType": "BR2",
          "BPTaxNumber": row["CNPJ/CPF"]
        },
        {
          "BPTaxType": "BR3",
          "BPTaxNumber": "ISENTO"
        }],

    "to_BusinessPartnerAddress": {
          "StreetName": row["LOGRADOURO"],                                                                      
          "HouseNumber": row["NÚMERO"],
          "District": row["BAIRRO/DISTRITO"],
          "PostalCode": row["CEP"],
          "CityName": row["MUNICÍPIO"],
          "Country": "BR",
          "Region": row["UF"],
          "Language": "PT",
          "to_EmailAddress": [
            {
              "EmailAddress": ""
            }
          ],
          "to_PhoneNumber": [
            {
              "DestinationLocationCountry": "BR",
              "PhoneNumber": ""
            }
          ]
        },
          "to_PhoneNumber":[
              {
                "PhoneNumber": "",
                "IsDefaultPhoneNumber": "false"
              }
            ],

    "to_Supplier": {
      "to_SupplierCompany": [
          {
            "CompanyCode": "LL4B",
            "ReconciliationAccount": "211001",
            "PaymentTerms": "NT00",
            "PaymentMethodsList": "NISTYZMJLV",
            "SupplierAccountGroup": "SUPL",
            "IsToBeCheckedForDuplicates": "true",
            "to_SupplierWithHoldingTax": []
          },
          {
            "CompanyCode": "LTEC",
            "ReconciliationAccount": "211001",
            "PaymentTerms": "NT00",
            "PaymentMethodsList": "NISTYZMJLV",
            "SupplierAccountGroup": "SUPL",
            "IsToBeCheckedForDuplicates": "true",
            "to_SupplierWithHoldingTax": []
          }
        ]
      },

      "to_SupplierPurchasingOrg": [
            {
              "PurchasingOrganization": "OC01",
              "PurchasingGroup": "",
              "PaymentTerms": "NT00",
              "PurchaseOrderCurrency": "BRL",
              "CalculationSchemaGroupCode": "R2",
              "InvoiceIsGoodsReceiptBased": "true",
        "InvoiceIsServiceBased": "true",
              "PurOrdAutoGenerationIsAllowed": "true",
        "DeletionIndicator": "false",
          "PurchasingIsBlockedForSupplier": "false",
              "to_PartnerFunction": [
                {
                  "PartnerFunction": "EP",
                  "ReferenceSupplier": ""
                },
                {
                  "PartnerFunction": "FN",
                  "ReferenceSupplier": ""
                },
                {
                  "PartnerFunction": "EF",
                  "ReferenceSupplier": ""
                }
              ]
            }
          ],
      "to_BusinessPartnerBank": [
        {
          "BankCountryKey": "BR",
          "BankNumber": row["CODIGO BANCO"],
          "bank_agency": row["AGENCIA"],
          "BankAccount": row["CONTA"],
          "BankControlKey": row["DIGITO CONTA"],
          "BankAccountName": row["NOME DO BANCO"]
        }
      ]  
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
