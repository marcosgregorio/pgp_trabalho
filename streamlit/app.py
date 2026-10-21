import random 
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. Configuração inicial
st.set_page_config(
    page_title="Monitor de Apreensões",
    layout="wide"
)

st.title("Assinatura de Apreensões: Mapeamento de Clusters (2025-2026)")


# 2. Carregamento dos dados
@st.cache_data
def carregar_dados():
    caminho = "../results/dataset_com_clusters_hdbscan_coordenadas.csv"

    dados = pd.read_csv(caminho)

    # Garantir que as coordenadas sejam numéricas
    dados["latitude"] = pd.to_numeric(
        dados["latitude"], errors="coerce"
    )
    dados["longitude"] = pd.to_numeric(
        dados["longitude"], errors="coerce"
    )

    dados["cluster_hdbscan"] = pd.to_numeric(
        dados["cluster_hdbscan"], errors="coerce"
    )

    # Remover registros sem coordenadas ou cluster
    dados = dados.dropna(
        subset=["latitude", "longitude", "cluster_hdbscan"]
    ).copy()

    dados["cluster_hdbscan"] = (
        dados["cluster_hdbscan"].astype(int)
    )

    return dados


df = carregar_dados()


# 3. Sidebar: filtros
st.sidebar.header("Filtros de Análise")

ufs = sorted(df["UF"].dropna().unique().tolist())
ufs_selecionadas = st.sidebar.multiselect(
    "UF:",
    ufs,
    default=ufs
)

df_filtrado = df[df["UF"].isin(ufs_selecionadas)]

municipios = sorted(
    df_filtrado["MUNICIPIO"].dropna().unique().tolist()
)
municipios_selecionados = st.sidebar.multiselect(
    "Município:",
    municipios,
    default=[]
)

if municipios_selecionados:
    df_filtrado = df_filtrado[
        df_filtrado["MUNICIPIO"].isin(municipios_selecionados)
    ]

tipos = sorted(
    df_filtrado["TIPO_OCORRENCIA"].dropna().unique().tolist()
)
tipos_selecionados = st.sidebar.multiselect(
    "Tipo de ocorrência:",
    tipos,
    default=tipos
)

df_filtrado = df_filtrado[
    df_filtrado["TIPO_OCORRENCIA"].isin(tipos_selecionados)
]

clusters = sorted(df_filtrado["cluster_hdbscan"].unique().tolist())
clusters_selecionados = st.sidebar.multiselect(
    "Clusters HDBSCAN:",
    clusters,
    default=clusters
)

df_filtrado = df_filtrado[
    df_filtrado["cluster_hdbscan"].isin(clusters_selecionados)
]


# 4. Cores dos clusters
def definir_cor(cluster_id):
    if cluster_id == -1:
        return "gray"

    # Cores determinísticas para diferentes clusters
    paleta = [
        "red", "blue", "orange", "green", "purple",
        "darkred", "cadetblue", "darkgreen", "pink",
        "darkblue", "lightblue", "beige", "black"
    ]

    return paleta[cluster_id % len(paleta)]


# 5. Indicadores
col1, col2, col3 = st.columns(3)

col1.metric("Registros no mapa", f"{len(df_filtrado):,}")
col2.metric(
    "Municípios",
    f"{df_filtrado['MUNICIPIO'].nunique():,}"
)
col3.metric(
    "Clusters identificados",
    int(
        df_filtrado.loc[
            df_filtrado["cluster_hdbscan"] != -1,
            "cluster_hdbscan"
        ].nunique()
    )
)


# 6. Construção do mapa
mapa = folium.Map(
    location=[-14.2350, -51.9253],
    zoom_start=4,
    tiles="OpenStreetMap"
)

deslocamento = 0.03 # eu que fiz isso aqui. eh pra evitar sobreposicao de pontos no mesmo municipio pq a ia nao entendia isso


for _, linha in df_filtrado.iterrows():
    cluster = linha["cluster_hdbscan"]
    cor = definir_cor(cluster)

    popup_html = f"""
    <b>Município:</b> {linha['MUNICIPIO']} - {linha['UF']}<br>
    <b>Tipo:</b> {linha['TIPO_OCORRENCIA']}<br>
    <b>Espécie:</b> {linha['ESPECIE_ARMA']}<br>
    <b>Marca:</b> {linha['MARCA_ARMA']}<br>
    <b>Calibre:</b> {linha['CALIBRE_ARMA']}<br>
    <b>Ano:</b> {linha['ANO_OCORRENCIA']}<br>
    <b>Cluster:</b> {cluster}<br>
    <b>Total:</b> {linha['TOTAL']}
    """

    nova_latitude = linha["latitude"] + (random.uniform(-deslocamento, deslocamento))
    nova_longitude = linha["longitude"] + (random.uniform(-deslocamento, deslocamento))

    folium.CircleMarker(
        location=[nova_latitude, nova_longitude],
        radius=6,
        color=cor,
        fill=True,
        fill_color=cor,
        fill_opacity=0.7,
        tooltip=f"{linha['MUNICIPIO']}/{linha['UF']} — Cluster {cluster}",
        popup=folium.Popup(popup_html, max_width=350)
    ).add_to(mapa)


# 7. Renderização
st_folium(mapa, width=None, height=650, use_container_width=True)


# 8. Legenda e contexto
st.markdown("""
### Como interpretar os clusters

- **Cinza (`-1`):** registros classificados pelo HDBSCAN como ruído,
  sem associação a um cluster.
- **Demais cores:** clusters identificados pelo algoritmo.

**Nota metodológica:** as coordenadas representam os centroides
geográficos dos municípios. Portanto, pontos no mesmo município podem
se sobrepor e não indicam o endereço exato de uma ocorrência.
""")
