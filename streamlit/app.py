import random 
import streamlit as st
import pandas as pd
import time
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


inicio_filtros = time.perf_counter()

df = carregar_dados()


# 3. Sidebar: filtros
st.sidebar.header("Filtros de Análise")

ufs = sorted(df["UF"].dropna().unique().tolist())
ufs_selecionadas = st.sidebar.multiselect(
    "UF:",
    ufs,
    default=[]
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

tempo_filtros = time.perf_counter() - inicio_filtros


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


# 6. Construção do mapa utilizando GeoJSON

inicio_construcao = time.perf_counter()

mapa = folium.Map(
    location=[-14.2350, -51.9253],
    zoom_start=4,
    tiles="OpenStreetMap",
    prefer_canvas=True
)

deslocamento = 0.03

colunas_mapa = [
    "latitude",
    "longitude",
    "cluster_hdbscan",
    "MUNICIPIO",
    "UF",
    "TIPO_OCORRENCIA",
    "ESPECIE_ARMA",
    "MARCA_ARMA",
    "CALIBRE_ARMA",
    "ANO_OCORRENCIA",
    "TOTAL"
]

dados_mapa = df_filtrado[colunas_mapa]


# Converter valores do Pandas para tipos compatíveis com JSON
def normalizar_valor(valor):
    if pd.isna(valor):
        return None

    if hasattr(valor, "item"):
        return valor.item()

    return valor


# Pré-calcular as cores dos clusters
clusters_mapa = dados_mapa["cluster_hdbscan"].unique()

cores_clusters = {
    int(cluster): definir_cor(int(cluster))
    for cluster in clusters_mapa
}


# Construir a coleção de pontos
features = []

for indice, linha in enumerate(
    dados_mapa.itertuples(index=True, name=None)
):

    (
        indice,
        latitude,
        longitude,
        cluster,
        municipio,
        uf,
        tipo,
        especie,
        marca,
        calibre,
        ano,
        total
    ) = linha

    cluster = int(cluster)

    gerador = random.Random(str(indice))

    nova_latitude = float(latitude) + gerador.uniform(
        -deslocamento,
        deslocamento
    )

    nova_longitude = float(longitude) + gerador.uniform(
        -deslocamento,
        deslocamento
    )

    propriedades = {
        "MUNICIPIO": normalizar_valor(municipio),
        "UF": normalizar_valor(uf),
        "TIPO_OCORRENCIA": normalizar_valor(tipo),
        "ESPECIE_ARMA": normalizar_valor(especie),
        "MARCA_ARMA": normalizar_valor(marca),
        "CALIBRE_ARMA": normalizar_valor(calibre),
        "ANO_OCORRENCIA": normalizar_valor(ano),
        "cluster_hdbscan": cluster,
        "TOTAL": normalizar_valor(total)
    }

    feature = {
        "type": "Feature",
        "id": str(indice),
        "geometry": {
            "type": "Point",
            "coordinates": [
                nova_longitude,
                nova_latitude
            ]
        },
        "properties": propriedades
    }

    features.append(feature)


# Criar a coleção GeoJSON
geojson_data = {
    "type": "FeatureCollection",
    "features": features
}


# Definir o estilo de cada registro conforme seu cluster
def estilo_cluster(feature):
    cluster = feature["properties"]["cluster_hdbscan"]
    cor = cores_clusters[cluster]

    return {
        "color": cor,
        "fillColor": cor,
        "fillOpacity": 0.7,
        "weight": 1
    }


# Criar a camada somente quando existem registros
if features:

    camada_registros = folium.GeoJson(
        data=geojson_data,

        name="Registros de apreensões",

        marker=folium.CircleMarker(
            radius=6,
            color="gray",
            fill=True,
            fill_color="gray",
            fill_opacity=0.7
        ),

        style_function=estilo_cluster,

        tooltip=folium.GeoJsonTooltip(
            fields=[
                "MUNICIPIO",
                "UF",
                "cluster_hdbscan"
            ],
            aliases=[
                "Município:",
                "UF:",
                "Cluster:"
            ],
            sticky=False
        ),

        popup=folium.GeoJsonPopup(
            fields=[
                "MUNICIPIO",
                "UF",
                "TIPO_OCORRENCIA",
                "ESPECIE_ARMA",
                "MARCA_ARMA",
                "CALIBRE_ARMA",
                "ANO_OCORRENCIA",
                "cluster_hdbscan",
                "TOTAL"
            ],
            aliases=[
                "Município:",
                "UF:",
                "Tipo:",
                "Espécie:",
                "Marca:",
                "Calibre:",
                "Ano:",
                "Cluster:",
                "Total:"
            ],
            localize=False
        )
    )

    camada_registros.add_to(mapa)


tempo_construcao = time.perf_counter() - inicio_construcao


# 7. Renderização

st_folium(
    mapa,
    key="mapa_apreensoes",
    returned_objects=[],
    width=None,
    height=650,
    use_container_width=True
)

# 8. Métricas da construção

st.markdown("### Desempenho do mapa")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Registros preparados",
    f"{len(dados_mapa):,}"
)

col2.metric(
    "Pontos individuais",
    f"{len(features):,}"
)

col3.metric(
    "Construção",
    f"{tempo_construcao:.3f} s"
)

print(
    f"[MAPA] Registros: {len(dados_mapa):,} | "
    f"Pontos: {len(features):,} | "
    f"Construção: {tempo_construcao:.3f}s"
)
