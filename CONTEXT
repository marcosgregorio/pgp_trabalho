# Pesquisa Acadêmica: Machine Learning Aplicado à Análise de Apreensões de Armas

**Data da Sessão:** 3 de Setembro de 2026  
**Foco:** Definição da problemática, viabilidade de dados públicos e estruturação de backlog para a Sprint 1.

## 1. Ideia Inicial e Restrições de Escopo
O objetivo é utilizar dados públicos de apreensões de armas e munições para identificar padrões espaciais e temporais via Machine Learning.  
**Limitação fundamental acordada:** Como dados abertos não possuem informações individualizadas (como números de série ou registros balísticos atrelados a indivíduos), a pesquisa **não** buscará determinar "procedência", "rastreio" ou "rotas de tráfico" diretas.

Em vez disso, a pesquisa focará em abordagens estatisticamente sólidas e defensáveis:
* Identificação de perfis/tipologias de municípios;
* Agrupamento espacial e/ou temporal;
* Descoberta de similaridades estruturais latentes.

## 2. A Escolha da Proposta: Clustering Espaço-Temporal/Estrutural
Após revisão da literatura (focada geralmente no hemisfério norte com dados restritos), identificou-se uma lacuna metodológica no Brasil. Enquanto institutos (como FBSP) fazem análises descritivas focadas em letalidade, esta pesquisa aplicará ML Não Supervisionado (Clustering) às armas em si.

**Tese Proposta:**  
Municípios geograficamente distantes podem compartilhar a mesma "assinatura criminal" de apreensão de armas (mesma sazonalidade, volume relativo e proporção de calibres). O uso de algoritmos como K-Means ou DBSCAN permite identificar tipologias latentes de apreensão que escapam aos relatórios agregados estaduais, sugerindo perfis logísticos ou de criminalidade similares independentes de fronteiras estaduais.

## 3. Exploração Inicial de Dados (Sprint 1)
O acesso ao sistema restrito SINESP foi contornado com a obtenção de dados consolidados publicamente via portal governamental (`OCORRENCIAS_2026.csv`).

**Descobertas do Dataset (ETL Inicial):**
* **Volume:** 75.776 registros.
* **Granularidade:** Possui Município, Estado e Mês de Ocorrência.
* **Características:** Inclui tipo de arma, calibre, marca e se o município tem mais de 1 milhão de habitantes.
* **Problema Identificado:** A coluna `TIPO_OCORRENCIA` possui uma quantidade significativa de valores vazios/nulos, o que exigirá limpeza na Sprint 2.
* **Padrão:** Há predominância de revólveres e espingardas nas ocorrências globais analisadas.

## 4. Engenharia de Features (Próximos Passos)
Para aplicar o modelo de clustering, as linhas de ocorrência individuais serão agrupadas em "Perfis Municipais", criando uma matriz onde cada linha é uma cidade.

Variáveis propostas para o modelo:
1. **Taxa Relativa:** Armas por 100 mil habitantes (requer cruzamento com população do IBGE).
2. **Proporção do "Mix" Criminal:** % de armas longas (espingardas) vs. armas curtas (revólveres).
3. **Frequência Temporal:** Sazonalidade (se os meses forem confiáveis) ou média mensal de apreensões.

## 5. Estruturação do Kanban (Backlog)
As tarefas abaixo foram definidas para guiar o andamento do projeto.

### 5.1 Pesquisa e Fundamentação
* [x] Ler artigos científicos sobre análise espacial de crimes e Machine Learning aplicado à segurança pública.
* [ ] Consolidar Referencial Teórico (Fichamento de 3-5 artigos chave sobre ML e análise espacial do crime).
* [ ] Definir a Pergunta de Pesquisa Oficial e a Hipótese baseada na literatura.

### 5.2 Preparação de Dados e Engenharia (Data Prep)
* [ ] **Limpeza de Dados:** Tratar valores nulos (especialmente em `TIPO_OCORRENCIA`) e normalizar nomes de municípios.
* [ ] **Enriquecimento:** Coletar dados populacionais do IBGE.
* [ ] **Feature Engineering:** Agrupar dados brutos para criar a matriz de *Perfis Municipais* (taxas, proporções, médias).

### 5.3 Modelagem (Machine Learning)
* [ ] **Normalização:** Aplicar `StandardScaler` (scikit-learn) nas features.
* [ ] **Otimização de K:** Rodar *Elbow Method* e *Silhouette Score* para definir o número ideal de clusters.
* [ ] **Treinamento K-Means:** Aplicar o algoritmo principal.
* [ ] **Treinamento Opcional:** Testar HDBSCAN para comparar a resiliência a *outliers* espaciais.

### 5.4 Avaliação e Visualização
* [ ] **Perfilamento:** Extrair estatísticas descritivas (média de características) de cada cluster gerado.
* [ ] **Visualização de Dados:** Criar Boxplots e gráficos comparativos dos clusters.
* [ ] **Mapeamento:** Plotar o mapa (via `geopandas`) colorindo municípios pelo cluster pertencente.

### 5.5 Redação Acadêmica
* [ ] Metodologia (justificativa do K-Means e limpeza).
* [ ] Resultados e Discussão (interpretação sociocriminal dos clusters).
* [ ] Limitações (viés de subnotificação e diferença entre apreensão policial vs. circulação real).
* [ ] Revisão Final.
