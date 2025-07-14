import pandas as pd
import json
from datetime import datetime

# Dados fictícios de vendas
data = [
    {"id": 1, "produto": "Notebook", "quantidade": 2, "valor": 3500.00},
    {"id": 2, "produto": "Mouse", "quantidade": 5, "valor": 150.00},
    {"id": 3, "produto": "Teclado", "quantidade": 3, "valor": 200.00},
]

df = pd.DataFrame(data)

tipo = input("Qual tipo de dado deseja gerar? (json/csv/parquet): ").strip().lower()

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

if tipo == "json":
    filename = f"vendas_{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Arquivo {filename} gerado.")
elif tipo == "csv":
    filename = f"vendas_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"Arquivo {filename} gerado.")
elif tipo == "parquet":
    filename = f"vendas_{timestamp}.parquet"
    df.to_parquet(filename, index=False)
    print(f"Arquivo {filename} gerado.")
else:
    print("Tipo não suportado. Escolha entre json, csv ou parquet.")
