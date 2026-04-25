import requests
import time


def extrair_dados_api(max_retries=3, delay=5):
    """
    Faz requisição à API com retry automático.

    Parâmetros:
        max_retries: número máximo de tentativas
        delay: tempo de espera entre tentativas (segundos)
    """

    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": "bitcoin,ethereum,solana",
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }

    tentativa = 0

    while tentativa < max_retries:
        try:
            print(f"Tentativa {tentativa + 1} de {max_retries}")

            response = requests.get(url, params=params, timeout=10)

            if response.status_code != 200:
                raise Exception(f"Erro na API: {response.status_code}")

            data = response.json()

            print("Dados extraídos com sucesso.")

            return data

        except Exception as e:
            print(f"Erro na tentativa {tentativa + 1}: {e}")

            tentativa += 1

            if tentativa < max_retries:
                print(f"Aguardando {delay} segundos para nova tentativa...")
                time.sleep(delay)
            else:
                print("Todas as tentativas falharam.")
                raise


if __name__ == "__main__":
    dados = extrair_dados_api()
    print(dados)