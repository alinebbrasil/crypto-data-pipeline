"""
04_create_analytics.py

Objetivo:
Criar uma camada analítica a partir dos dados processados de criptomoedas.

Entrada:
- data/processed/crypto_prices.parquet

Saída:
- data/analytics/crypto_analytics.parquet
- data/analytics/crypto_analytics.csv

Essa camada será usada pelo dashboard Streamlit.
"""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "crypto_prices.parquet"
ANALYTICS_DATA_DIR = PROJECT_ROOT / "data" / "analytics"

OUTPUT_PARQUET = ANALYTICS_DATA_DIR / "crypto_analytics.parquet"
OUTPUT_CSV = ANALYTICS_DATA_DIR / "crypto_analytics.csv"


def criar_pasta_se_nao_existir(path: Path) -> None:
    """
    Cria uma pasta caso ela ainda não exista.
    """
    path.mkdir(parents=True, exist_ok=True)


def carregar_dados_processados(filepath: Path) -> pd.DataFrame:
    """
    Carrega a base processada em Parquet.
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")

    df = pd.read_parquet(filepath)

    if df.empty:
        raise ValueError("A base processada está vazia.")

    return df


def preparar_base_analitica(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepara a base analítica com cálculos úteis para monitoramento.
    """
    df = df.copy()

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["price_usd"] = pd.to_numeric(df["price_usd"], errors="coerce")
    df["price_change_percentage_24h"] = pd.to_numeric(
        df["price_change_percentage_24h"],
        errors="coerce",
    )

    df = df.dropna(subset=["timestamp", "crypto_id", "price_usd"])

    df = df.drop_duplicates(subset=["timestamp", "crypto_id"])

    df = df.sort_values(["crypto_id", "timestamp"])

    df["previous_price_usd"] = df.groupby("crypto_id")["price_usd"].shift(1)

    df["price_change_since_last_collect"] = (
        df["price_usd"] - df["previous_price_usd"]
    )

    df["price_change_pct_since_last_collect"] = (
        df["price_change_since_last_collect"] / df["previous_price_usd"]
    ) * 100

    df["movement_status"] = df["price_change_since_last_collect"].apply(
        classificar_movimento
    )

    df["date"] = df["timestamp"].dt.date
    df["hour"] = df["timestamp"].dt.hour

    return df


def classificar_movimento(value: float) -> str:
    """
    Classifica o movimento do preço entre uma coleta e outra.
    """
    if pd.isna(value):
        return "sem histórico anterior"

    if value > 0:
        return "alta"

    if value < 0:
        return "queda"

    return "estável"


def salvar_base_analitica(df: pd.DataFrame) -> None:
    """
    Salva a camada analytics em Parquet e CSV.
    """
    df.to_parquet(OUTPUT_PARQUET, index=False)
    df.to_csv(OUTPUT_CSV, index=False)

    print(f"Parquet salvo em: {OUTPUT_PARQUET}")
    print(f"CSV salvo em: {OUTPUT_CSV}")
    print(f"Total de registros: {len(df)}")


def main() -> None:
    """
    Executa a criação da camada analytics.
    """
    print("Criando camada analytics...")

    criar_pasta_se_nao_existir(ANALYTICS_DATA_DIR)

    df = carregar_dados_processados(PROCESSED_DATA_PATH)
    df_analytics = preparar_base_analitica(df)

    salvar_base_analitica(df_analytics)

    print("Camada analytics criada com sucesso.")


if __name__ == "__main__":
    main()