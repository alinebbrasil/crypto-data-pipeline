def validar_dados_api(data: object) -> None:
    """
    Valida se a API retornou dados.

    Aceita dois formatos:
    1. Lista de moedas
    2. Dicionário com moedas como chave
    """
    if data is None:
        raise ValueError("A API retornou None.")

    if isinstance(data, list) and len(data) == 0:
        raise ValueError("A API retornou uma lista vazia.")

    if isinstance(data, dict) and len(data) == 0:
        raise ValueError("A API retornou um dicionário vazio.")

    if not isinstance(data, (list, dict)):
        raise ValueError("Formato inesperado: esperado lista ou dicionário.")


def preparar_payload_raw(data: object) -> dict:
    """
    Adiciona metadados à resposta bruta da API.

    Aceita dados em lista ou dicionário.
    """
    records_count = len(data) if isinstance(data, (list, dict)) else 0

    return {
        "metadata": {
            "source": "CoinGecko API",
            "collected_at": datetime.now().isoformat(timespec="seconds"),
            "records_count": records_count,
        },
        "data": data,
    }