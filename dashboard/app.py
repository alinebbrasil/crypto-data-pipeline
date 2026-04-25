import pandas as pd
import streamlit as st

# configuração geral da página
st.set_page_config(
    page_title="Crypto Market Dashboard",
    layout="wide"
)

# caminho do arquivo tratado em formato parquet
DATA_PATH = "data/processed/crypto_prices.parquet"


def carregar_dados(path: str) -> pd.DataFrame:
    """
    Carrega os dados processados do pipeline.

    O arquivo parquet é gerado pelo script 03_transform_raw.py.
    """
    df = pd.read_parquet(path)

    # garante que a coluna timestamp esteja no formato de data/hora
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    return df


# carregamento dos dados
df = carregar_dados(DATA_PATH)

# título principal
st.title("Crypto Market Dashboard")

# descrição do dashboard
st.write(
    "Dashboard para acompanhamento de preços de criptomoedas coletados via API "
    "e atualizados por pipeline orquestrado com Airflow."
)

# métricas gerais do dataset
st.subheader("Métricas gerais")

col1, col2, col3 = st.columns(3)

col1.metric("Total de registros", len(df))
col2.metric("Criptomoedas monitoradas", df["crypto"].nunique())
col3.metric("Última atualização", df["timestamp"].max().strftime("%d/%m/%Y %H:%M:%S"))

# seleção da criptomoeda
st.subheader("Análise por criptomoeda")

cryptos = sorted(df["crypto"].unique())

crypto_selecionada = st.selectbox(
    "Selecione a criptomoeda",
    cryptos
)

# filtra os dados da criptomoeda selecionada
df_filtrado = df[df["crypto"] == crypto_selecionada].copy()

# ordena os dados por timestamp para garantir linha temporal correta
df_filtrado = df_filtrado.sort_values("timestamp")

# captura os valores mais recentes
ultimo_registro = df_filtrado.iloc[-1]

# indicadores da criptomoeda selecionada
col1, col2, col3 = st.columns(3)

col1.metric(
    "Preço atual (USD)",
    round(ultimo_registro["price_usd"], 2)
)

col2.metric(
    "Variação 24h (%)",
    round(ultimo_registro["change_24h"], 2)
)

col3.metric(
    "Total de capturas",
    len(df_filtrado)
)

# tabela com os dados filtrados
st.subheader("Dados históricos")

st.dataframe(
    df_filtrado[[
        "timestamp",
        "crypto",
        "price_usd",
        "change_24h"
    ]]
)

# gráfico de evolução do preço
st.subheader("Histórico de preço")

st.line_chart(
    df_filtrado,
    x="timestamp",
    y="price_usd"
)

# gráfico de variação percentual em 24h
st.subheader("Variação percentual em 24h")

st.line_chart(
    df_filtrado,
    x="timestamp",
    y="change_24h"
)