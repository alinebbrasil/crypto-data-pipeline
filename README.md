# Crypto Real-Time Monitoring Pipeline

## Visão Geral

Este projeto apresenta um pipeline de dados para monitoramento de criptomoedas em tempo quase real, utilizando ingestão via API, organização em camadas de dados e visualização interativa com Streamlit.

O objetivo é simular um fluxo moderno de dados, no qual informações são coletadas periodicamente, armazenadas em formato bruto, transformadas para análise e disponibilizadas em um dashboard com atualização automática.

---

## Arquitetura do Projeto

O fluxo do pipeline segue a estrutura:

API CoinGecko → Camada RAW → Camada PROCESSED → Camada ANALYTICS → Dashboard Streamlit

---

## Camadas de Dados

### RAW

A camada RAW armazena os dados brutos coletados da API em arquivos JSON.

Essa camada preserva a resposta original da fonte, permitindo rastreabilidade e reprocessamento posterior.

### PROCESSED

A camada PROCESSED transforma os arquivos JSON em uma estrutura tabular, salvando os dados em CSV e Parquet.

Essa etapa organiza os campos principais, como criptomoeda, timestamp, preço e variação percentual.

### ANALYTICS

A camada ANALYTICS prepara os dados para consumo analítico no dashboard.

Foram criadas métricas como:

* preço anterior
* variação desde a última coleta
* variação percentual desde a última coleta
* status de movimento (alta, queda ou estável)

---

## Pipeline

O projeto conta com um runner único para executar todas as etapas do pipeline em sequência:

1. Coleta dos dados da API
2. Salvamento dos dados brutos em JSON
3. Transformação dos dados para camada processada
4. Criação da camada analítica

Para executar o pipeline completo:

```bash
python scripts/run_pipeline.py
```

---

## Dashboard

O dashboard foi desenvolvido em Streamlit e consome a camada ANALYTICS.

Ele apresenta:

* total de registros coletados
* quantidade de criptomoedas monitoradas
* quantidade de arquivos processados
* última atualização da base
* preço atual por criptomoeda
* variação percentual em 24h
* variação desde a última coleta
* status de movimento
* histórico de preços
* tabela com dados históricos

O dashboard possui atualização automática da visualização, simulando um monitoramento em tempo quase real.

Para executar:

```bash
streamlit run dashboard/app.py
```

ou:

```bash
python -m streamlit run dashboard/app.py
```

---

## Tecnologias Utilizadas

* Python
* pandas
* API CoinGecko
* JSON
* Parquet
* Streamlit
* streamlit-autorefresh
* Airflow
* ETL
* Data Pipeline
* Data Analytics

---

## Estrutura do Projeto

```text
crypto-data-pipeline/
│
├── dags/
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── analytics/
│
├── scripts/
│   ├── api_extract.py
│   ├── 02_save_raw_json.py
│   ├── 03_transform_raw.py
│   ├── 04_create_analytics.py
│   └── run_pipeline.py
│
├── requirements.txt
└── README.md
```

---

## Como Executar o Projeto

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Executar o pipeline completo

```bash
python scripts/run_pipeline.py
```

### 3. Abrir o dashboard

```bash
streamlit run dashboard/app.py
```

---

## Principais Aprendizados

* construção de pipeline com ingestão via API
* organização de dados em camadas RAW, PROCESSED e ANALYTICS
* transformação de dados brutos em base analítica
* criação de métricas de variação entre coletas
* uso de Parquet para armazenamento analítico
* desenvolvimento de dashboard com atualização automática
* simulação de monitoramento em tempo quase real

---

## Insight Técnico

O projeto evoluiu de um dashboard simples de criptomoedas para um pipeline estruturado, com separação clara entre coleta, transformação, camada analítica e visualização.

Essa arquitetura melhora a organização, facilita manutenção e aproxima o projeto de um fluxo real utilizado em ambientes de dados.

---

## Autora

Aline Bastos Brasil

Analista de Dados | SQL | Python | Power BI | ETL & Data Pipelines

LinkedIn: https://www.linkedin.com/in/alinebbrasildata/
