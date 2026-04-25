import os
import pandas as pd

# arquivo tratado gerado no script 03
INPUT_FILE = "data/processed/crypto_prices.csv"

# arquivo analítico final
OUTPUT_FILE = "data/processed/crypto_analytics.csv"


def validar_arquivo(path: str):
    """
    Verifica se o arquivo tratado existe antes de iniciar a análise.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")


def criar_tabela_analitica():
    """
    Cria uma tabela analítica por criptomoeda.

    Como cada execução da API gera novas capturas,
    esta etapa resume o histórico disponível.
    """
    df = pd.read_csv(INPUT_FILE)

    analytics = (
        df.groupby("crypto")
        .agg(
            preco_medio_usd=("price_usd", "mean"),
            preco_minimo_usd=("price_usd", "min"),
            preco_maximo_usd=("price_usd", "max"),
            variacao_media_24h=("change_24h", "mean"),
            total_capturas=("crypto", "count")
        )
        .reset_index()
    )

    analytics.to_csv(OUTPUT_FILE, index=False)

    print(f"Tabela analítica salva em: {OUTPUT_FILE}")
    print(analytics)


def main():
    """
    Pipeline analítico:

    1. Valida arquivo tratado
    2. Agrupa dados por criptomoeda
    3. Gera métricas resumidas
    4. Salva tabela analítica
    """
    print("Iniciando criação da camada analítica...")

    validar_arquivo(INPUT_FILE)
    criar_tabela_analitica()

    print("Camada analítica criada com sucesso.")


if __name__ == "__main__":
    main()