"""
app.py

Dashboard Streamlit para monitoramento de criptomoedas em tempo quase real.

Fonte:
- data/analytics/crypto_analytics.parquet

Para executar:
streamlit run dashboard/app.py
"""

from pathlib import Path

import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh


st.set_page_config(
    page_title="Crypto Real-Time Monitoring",
    layout="wide"
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "analytics" / "crypto_analytics.parquet"


# Atualiza a tela automaticamente a cada 60 segundos
st_autorefresh(interval=60 * 1000, key="crypto_dashboard_refresh")


@st.cache_data(ttl=60)
def carregar_dados(path: Path) -> pd.DataFrame:
    """
    Carrega a camada analytics do pipeline.

    Args:
        path: caminho do arquivo Parquet.

    Returns:
        DataFrame com dados analíticos de criptomoedas.
    """
    if not path.exists():
        st.error(f"Arquivo não encontrado: {path}")
        st.stop()

    df = pd.read_parquet(path)

    if df.empty:
        st.error("A base analytics está vazia.")
        st.stop()

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    return df


def formatar_moeda(valor: float) -> str:
    """
    Formata valores monetários em dólar.
    """
    return f"US$ {valor:,.2f}"


def formatar_percentual(valor: float) -> str:
    """
    Formata valores percentuais.
    """
    if pd.isna(valor):
        return "N/A"

    return f"{valor:.2f}%"


df = carregar_dados(DATA_PATH)

st.title("Crypto Real-Time Monitoring Dashboard")

st.write(
    "Dashboard para monitoramento de criptomoedas com ingestão incremental, "
    "camadas de dados RAW, PROCESSED e ANALYTICS, e atualização automática da visualização."
)

ultima_atualizacao = df["timestamp"].max()

st.caption(
    f"Última atualização da base: {ultima_atualizacao.strftime('%d/%m/%Y %H:%M:%S')}"
)

st.subheader("Visão geral")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total de registros", len(df))
col2.metric("Criptomoedas monitoradas", df["crypto_id"].nunique())
col3.metric("Arquivos processados", df["source_file"].nunique())
col4.metric("Status", "Atualização automática")

st.divider()

st.subheader("Análise por criptomoeda")

cryptos = sorted(df["crypto_id"].dropna().unique())

crypto_selecionada = st.selectbox(
    "Selecione a criptomoeda",
    cryptos
)

df_filtrado = df[df["crypto_id"] == crypto_selecionada].copy()
df_filtrado = df_filtrado.sort_values("timestamp")

ultimo_registro = df_filtrado.iloc[-1]

preco_atual = ultimo_registro["price_usd"]
variacao_24h = ultimo_registro["price_change_percentage_24h"]
variacao_ultima_coleta = ultimo_registro["price_change_pct_since_last_collect"]
status_movimento = ultimo_registro["movement_status"]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Preço atual",
    formatar_moeda(preco_atual)
)

col2.metric(
    "Variação 24h",
    formatar_percentual(variacao_24h)
)

col3.metric(
    "Variação desde última coleta",
    formatar_percentual(variacao_ultima_coleta)
)

col4.metric(
    "Movimento",
    status_movimento
)

st.divider()

st.subheader("Histórico de preço")

st.line_chart(
    df_filtrado,
    x="timestamp",
    y="price_usd"
)

st.subheader("Variação percentual desde a última coleta")

st.line_chart(
    df_filtrado,
    x="timestamp",
    y="price_change_pct_since_last_collect"
)

st.subheader("Dados históricos")

st.dataframe(
    df_filtrado[
        [
            "timestamp",
            "crypto_id",
            "price_usd",
            "previous_price_usd",
            "price_change_since_last_collect",
            "price_change_pct_since_last_collect",
            "price_change_percentage_24h",
            "movement_status",
            "source_file",
        ]
    ],
    use_container_width=True
)