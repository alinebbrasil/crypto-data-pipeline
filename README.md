# Crypto Data Pipeline

Projeto de engenharia de dados para ingestão, processamento e análise de dados de criptomoedas em tempo quase real, utilizando API pública, orquestração com Airflow e visualização com Streamlit.

## Objetivo

Construir um pipeline de dados completo que simula um cenário real de ingestão contínua, processamento em camadas e disponibilização de dados para análise.

## Arquitetura do Projeto

O pipeline segue a seguinte estrutura:

API → Ingestão → Camada Raw → Transformação → Camada Processed → Camada Analítica → Dashboard

## Tecnologias Utilizadas

* Python
* Pandas
* Requests
* Apache Airflow
* Docker
* Parquet
* Streamlit

## Estrutura do Projeto

```
crypto-data-pipeline/
├── airflow/
│   ├── dags/
│   │   └── crypto_pipeline_dag.py
│   └── docker-compose.yml
├── dashboard/
│   └── app.py
├── data/
│   ├── raw/
│   └── processed/
├── scripts/
│   ├── api_extract.py
│   ├── 02_save_raw_json.py
│   ├── 03_transform_raw.py
│   └── 04_create_analytics.py
├── requirements.txt
└── README.md
```

## Etapas do Pipeline

### 1. Extração de Dados

* Consumo de API pública de criptomoedas
* Implementação de retry automático em caso de falha
* Dados retornados em formato JSON

### 2. Camada Raw

* Armazenamento dos dados brutos em arquivos JSON
* Versionamento por timestamp

### 3. Transformação

* Leitura dos arquivos JSON
* Estruturação dos dados em formato tabular
* Inclusão de timestamp de coleta
* Salvamento em CSV e Parquet

### 4. Camada Analítica

* Agregação de dados por criptomoeda
* Cálculo de métricas como:

  * preço médio
  * preço mínimo e máximo
  * variação média
  * número de capturas

### 5. Orquestração com Airflow

* Execução automática do pipeline a cada 5 minutos
* Controle de dependências entre tarefas
* Implementação de retry em caso de falha

### 6. Dashboard com Streamlit

* Visualização dos dados em tempo quase real
* Filtro por criptomoeda
* Indicadores principais:

  * preço atual
  * variação percentual
  * número de registros
* Gráficos de evolução temporal

## Execução do Projeto

### Rodar pipeline manualmente

```
python scripts/02_save_raw_json.py
python scripts/03_transform_raw.py
python scripts/04_create_analytics.py
```

### Rodar Airflow com Docker

```
cd airflow
docker-compose up
```

Acessar:
http://localhost:8080

Login:
admin / admin

### Rodar dashboard

```
python -m streamlit run dashboard/app.py
```

Acessar:
http://localhost:8501

## Diferenciais do Projeto

* Pipeline com dados em atualização contínua (API)
* Arquitetura em camadas (raw, processed, analytics)
* Uso de formato Parquet
* Orquestração com Airflow
* Tratamento de falhas com retry
* Dashboard interativo

## Possíveis Evoluções

* Integração com AWS S3 ou Azure
* Uso de banco de dados analítico
* Streaming em tempo real (Kafka)
* Alertas automáticos
* Deploy do dashboard

## Autor

Aline Bastos Brasil
https://www.linkedin.com/in/alinebbrasil/
