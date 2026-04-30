"""
03_transform_raw.py

Objetivo:
Transformar os arquivos JSON da camada RAW em uma tabela estruturada.

Compatível com:
1. Formato antigo (dict):
   {"bitcoin": {"usd": 100, "usd_24h_change": 2}}

2. Formato novo (payload com metadata):
   {"metadata": {...}, "data": [...]}
"""

import json
from datetime import datetime
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_CSV = PROCESSED_DATA_DIR / "crypto_prices.csv"
OUTPUT_PARQUET = PROCESSED_DATA_DIR / "crypto_prices.parquet"


def criar_pasta_se_nao_existir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def listar_arquivos_json(input_dir: Path):
    arquivos = sorted(input_dir.glob("*.json"))

    if not arquivos:
        raise FileNotFoundError("Nenhum arquivo JSON encontrado em data/raw.")

    return arquivos


def extrair_timestamp_do_nome_arquivo(filepath: Path):
    timestamp_texto = filepath.stem.replace("crypto_", "")
    return datetime.strptime(timestamp_texto, "%Y-%m-%d_%H-%M-%S")


def carregar_json(filepath: Path):
    with filepath.open("r", encoding="utf-8") as file:
        return json.load(file)


def transformar_payload(payload):
    """
    Converte qualquer formato da API para uma lista padronizada
    """

    # FORMATO NOVO (com metadata + lista)
    if isinstance(payload, dict) and "data" in payload:
        dados = payload["data"]

        # se já for lista (CoinGecko markets)
        if isinstance(dados, list):
            return dados

        # se for dict dentro de data
        if isinstance(dados, dict):
            return [
                {
                    "id": moeda,
                    "current_price": valores.get("usd"),
                    "price_change_percentage_24h": valores.get("usd_24h_change"),
                }
                for moeda, valores in dados.items()
            ]

    # FORMATO ANTIGO (dict direto)
    if isinstance(payload, dict):
        return [
            {
                "id": moeda,
                "current_price": valores.get("usd"),
                "price_change_percentage_24h": valores.get("usd_24h_change"),
            }
            for moeda, valores in payload.items()
        ]

    # FORMATO LISTA (já pronto)
    if isinstance(payload, list):
        return payload

    raise ValueError("Formato de payload não reconhecido.")


def transformar_arquivos_em_dataframe(arquivos):
    linhas = []

    for filepath in arquivos:
        timestamp = extrair_timestamp_do_nome_arquivo(filepath)
        payload = carregar_json(filepath)

        dados = transformar_payload(payload)

        for item in dados:
            linhas.append(
                {
                    "timestamp": timestamp,
                    "crypto_id": item.get("id"),
                    "symbol": item.get("symbol"),
                    "crypto_name": item.get("name"),
                    "price_usd": item.get("current_price"),
                    "price_change_percentage_24h": item.get(
                        "price_change_percentage_24h"
                    ),
                    "source_file": filepath.name,
                }
            )

    df = pd.DataFrame(linhas)

    if df.empty:
        raise ValueError("Nenhum dado foi transformado.")

    return df


def limpar_dataframe(df):
    df = df.copy()

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["price_usd"] = pd.to_numeric(df["price_usd"], errors="coerce")
    df["price_change_percentage_24h"] = pd.to_numeric(
        df["price_change_percentage_24h"], errors="coerce"
    )

    df = df.dropna(subset=["crypto_id", "price_usd"])

    df = df.drop_duplicates(subset=["timestamp", "crypto_id"])

    df = df.sort_values(["crypto_id", "timestamp"])

    return df


def salvar_dataframe(df):
    df.to_csv(OUTPUT_CSV, index=False)
    df.to_parquet(OUTPUT_PARQUET, index=False)

    print(f"CSV salvo em: {OUTPUT_CSV}")
    print(f"Parquet salvo em: {OUTPUT_PARQUET}")
    print(f"Total de registros: {len(df)}")


def main():
    print("Iniciando transformação...")

    criar_pasta_se_nao_existir(PROCESSED_DATA_DIR)

    arquivos = listar_arquivos_json(RAW_DATA_DIR)
    df = transformar_arquivos_em_dataframe(arquivos)
    df = limpar_dataframe(df)

    salvar_dataframe(df)

    print("Transformação concluída.")


if __name__ == "__main__":
    main()