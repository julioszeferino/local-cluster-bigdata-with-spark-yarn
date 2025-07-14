import pandas as pd
import json
from datetime import datetime

# Dados fictícios de estoque
data = [
    {"id": 1, "produto": "Notebook", "quantidade_estoque": 10, "local": "Almoxarifado A"},
    {"id": 2, "produto": "Mouse", "quantidade_estoque": 50, "local": "Almoxarifado B"},
    {"id": 3, "produto": "Teclado", "quantidade_estoque": 30, "local": "Almoxarifado A"},
]

df = pd.DataFrame(data)

tipo = input("Qual tipo de dado deseja gerar? (json/csv/parquet): ").strip().lower()

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

if tipo == "json":
    filename = f"estoque_{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Arquivo {filename} gerado.")
elif tipo == "csv":
    filename = f"estoque_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"Arquivo {filename} gerado.")
elif tipo == "parquet":
    filename = f"estoque_{timestamp}.parquet"
    df.to_parquet(filename, index=False)
    print(f"Arquivo {filename} gerado.")
else:
    print("Tipo não suportado. Escolha entre json, csv ou parquet.")
