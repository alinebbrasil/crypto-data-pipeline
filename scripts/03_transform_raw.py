import json
import os
from datetime import datetime

import pandas as pd

# pasta onde estão os arquivos JSON brutos
INPUT_DIR = "data/raw"

# pasta onde os arquivos tratados serão salvos
OUTPUT_DIR = "data/processed"

# arquivos finais da camada processed
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "crypto_prices.csv")
OUTPUT_PARQUET = os.path.join(OUTPUT_DIR, "crypto_prices.parquet")


def criar_pasta_se_nao_existir(path: str):
    """
    Cria a pasta de saída caso ela ainda não exista.
    """
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Pasta criada: {path}")


def ler_arquivos_json(input_dir: str):
    """
    Lê todos os arquivos JSON da pasta raw.
    Cada arquivo representa uma captura da API.
    """
    arquivos = [
        arquivo for arquivo in os.listdir(input_dir)
        if arquivo.endswith(".json")
    ]

    if not arquivos:
        raise FileNotFoundError("Nenhum arquivo JSON encontrado em data/raw.")

    return arquivos


def extrair_timestamp_do_nome_arquivo(arquivo: str):
    """
    Extrai o timestamp a partir do nome do arquivo.

    Exemplo:
    crypto_2026-04-25_15-30-00.json
    """
    timestamp_texto = arquivo.replace("crypto_", "").replace(".json", "")

    return datetime.strptime(timestamp_texto, "%Y-%m-%d_%H-%M-%S")


def transformar_json_em_linhas(arquivos):
    """
    Transforma os JSONs da API em uma estrutura tabular.

    Cada criptomoeda vira uma linha com:
    - timestamp da coleta
    - nome da moeda
    - preço em dólar
    - variação percentual em 24h
    - arquivo de origem
    """
    linhas = []

    for arquivo in arquivos:
        caminho = os.path.join(INPUT_DIR, arquivo)
        timestamp = extrair_timestamp_do_nome_arquivo(arquivo)

        with open(caminho, "r") as f:
            dados = json.load(f)

        for moeda, valores in dados.items():
            linhas.append({
                "timestamp": timestamp,
                "crypto": moeda,
                "price_usd": valores.get("usd"),
                "change_24h": valores.get("usd_24h_change"),
                "source_file": arquivo
            })

    return linhas


def salvar_tabela(linhas):
    """
    Salva os dados transformados em CSV e Parquet.
    """
    df = pd.DataFrame(linhas)

    df.to_csv(OUTPUT_CSV, index=False)
    df.to_parquet(OUTPUT_PARQUET, index=False)

    print(f"Arquivo CSV salvo em: {OUTPUT_CSV}")
    print(f"Arquivo Parquet salvo em: {OUTPUT_PARQUET}")
    print(f"Total de registros: {len(df)}")


def main():
    """
    Pipeline de transformação:

    1. Localiza arquivos JSON brutos
    2. Extrai timestamp do nome dos arquivos
    3. Converte JSON em tabela
    4. Salva camada processed em CSV e Parquet
    """
    print("Iniciando transformação dos dados brutos...")

    criar_pasta_se_nao_existir(OUTPUT_DIR)

    arquivos = ler_arquivos_json(INPUT_DIR)

    linhas = transformar_json_em_linhas(arquivos)

    salvar_tabela(linhas)

    print("Transformação concluída com sucesso.")


if __name__ == "__main__":
    main()