import json
import os
from datetime import datetime
from api_extract import extrair_dados_api

# pasta onde os dados serão armazenados
OUTPUT_DIR = "data/raw"


def criar_pasta_se_nao_existir(path: str):
    """
    Cria diretório caso ele ainda não exista.
    """
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Pasta criada: {path}")


def gerar_nome_arquivo():
    """
    Gera nome de arquivo baseado no timestamp atual.

    Exemplo:
        crypto_2026-04-25_15-30-00.json
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"crypto_{timestamp}.json"


def salvar_json(data: dict, path: str):
    """
    Salva dados em formato JSON no caminho especificado.
    """
    with open(path, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Arquivo salvo em: {path}")


def main():
    """
    Pipeline de ingestão:

    1. Cria pasta raw (se necessário)
    2. Extrai dados da API
    3. Gera nome de arquivo com timestamp
    4. Salva dados em JSON
    """

    print("Iniciando pipeline de ingestão...")

    # garante que a pasta existe
    criar_pasta_se_nao_existir(OUTPUT_DIR)

    # extrai dados da API
    data = extrair_dados_api()

    # gera nome do arquivo
    filename = gerar_nome_arquivo()

    # caminho completo
    filepath = os.path.join(OUTPUT_DIR, filename)

    # salva o JSON
    salvar_json(data, filepath)

    print("Pipeline finalizado com sucesso.")


if __name__ == "__main__":
    main()