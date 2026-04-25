from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

"""
DAG: crypto_data_pipeline

Objetivo:
Orquestrar um pipeline de dados de criptomoedas via API.

Etapas:
1. Extrair dados da API e salvar JSON bruto
2. Transformar JSONs em tabela processada
3. Criar camada analítica

Configuração:
- Execução a cada 5 minutos
- Retry automático em caso de falha
"""

with DAG(
    dag_id="crypto_data_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="*/5 * * * *",
    catchup=False,
    description="Pipeline de dados de criptomoedas via API com retry automático",
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=1),
    },
) as dag:

    extract_api = BashOperator(
        task_id="extract_api",
        bash_command="cd /opt/airflow && python scripts/02_save_raw_json.py",
    )

    transform_data = BashOperator(
        task_id="transform_data",
        bash_command="cd /opt/airflow && python scripts/03_transform_raw.py",
    )

    create_analytics = BashOperator(
        task_id="create_analytics",
        bash_command="cd /opt/airflow && python scripts/04_create_analytics.py",
    )

    extract_api >> transform_data >> create_analytics