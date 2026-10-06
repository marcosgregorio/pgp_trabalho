import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. Configuração Inicial da Página
st.set_page_config(page_title="Monitor de Apreensões", layout="wide")
st.title("Assinatura de Apreensões: Mapeamento de Clusters (2025-2026)")

# 2. Carregamento dos Dados (com Cache para performance)
@st.cache_data
def carregar_dados():
    # Em um cenário real: pd.read_csv('data/apreensoes_com_clusters.csv')
    # Aqui criamos dados fictícios simulando o resultado do seu DBSCAN/HDBSCAN
    dados = pd.DataFrame({
        'lat': [-27.1, -27.12, -23.5, -23.55, -15.8, -15.7],
        'lon': [-52.6, -52.61, -46.6, -46.65, -47.9, -47.8],
        'motivo': ['Tráfico', 'Tráfico', 'Feminicídio', 'Briga', 'Tráfico', 'Tráfico'],
        'cluster': [0, 0, -1, 1, 2, 2] # -1 é o ruído do DBSCAN
    })
    return dados

df = carregar_dados()

# 3. Barra Lateral (Sidebar) para Filtros Interativos
st.sidebar.header("Filtros de Análise")

motivos = df['motivo'].unique().tolist()
motivo_selecionado = st.sidebar.multiselect("Motivo da Apreensão:", motivos, default=motivos)

# Aplicar o filtro no dataframe
df_filtrado = df[df['motivo'].isin(motivo_selecionado)]

# 4. Função para definir as cores baseadas no Cluster
def definir_cor(cluster_id):
    if cluster_id == -1:
        return 'gray'    # Ruído (apreensões isoladas)
    elif cluster_id == 0:
        return 'red'     # Cluster 0 (ex: Chapecó/SC)
    elif cluster_id == 1:
        return 'blue'    # Cluster 1 (ex: São Paulo/SP)
    else:
        return 'orange'  # Cluster 2, etc.

# 5. Construção do Mapa com Folium (Leaflet)
# Centralizando o mapa no Brasil
mapa = folium.Map(location=[-15.7801, -47.9292], zoom_start=4)
# Adicionando os pontos filtrados ao mapa
for _, linha in df_filtrado.iterrows():
    folium.CircleMarker(
        location=[linha['lat'], linha['lon']],
        radius=6,
        color=definir_cor(linha['cluster']),
        fill=True,
        fill_color=definir_cor(linha['cluster']),
        fill_opacity=0.7,
        tooltip=f"Motivo: {linha['motivo']} | Cluster: {linha['cluster']}"
    ).add_to(mapa)

# 6. Renderizando o mapa no Streamlit
st_folium(mapa, width=1200, height=600)

st.markdown("""
> **Análise da Desorganização Social:** Pontos em cinza representam o cluster `-1` (ruído/ocorrências isoladas). 
Aglomerados coloridos representam assinaturas criminais detectadas pelos algoritmos espaciais.
""")