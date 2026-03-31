#stramlit run dashboard.py
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title(" Análise de Avaliações de Filmes - MovieLens 100K")

# Carregar dados com cache
@st.cache_data
def load_data():
    ratings = pd.read_csv('ml-100k/u.data', sep='\t', names=['user_id', 'movie_id', 'rating', 'timestamp'])
    movies = pd.read_csv('ml-100k/u.item', sep='|', encoding='latin-1',
                         names=['movie_id', 'title'] + ['col' + str(i) for i in range(22)],
                         usecols=[0, 1])
    df = pd.merge(ratings, movies, on='movie_id')
    return df

df = load_data()

# SIDEBAR - Filtros
st.sidebar.header("🎛️ Filtros")
min_ratings = st.sidebar.slider("Avaliações mínimas por filme", 0, 300, 100)

# Análise: Melhores Filmes
st.subheader("🏆 Melhores Filmes com pelo menos {} avaliações".format(min_ratings))
count_ratings = df.groupby('title')['rating'].count()
mean_ratings = df.groupby('title')['rating'].mean()
filtered_titles = count_ratings[count_ratings >= min_ratings].index
top_movies = mean_ratings[filtered_titles].sort_values(ascending=False).head(10)
st.dataframe(top_movies)

# Análise: Piores Filmes
st.subheader("💔 Piores Filmes com pelo menos {} avaliações".format(min_ratings))
worst_movies = mean_ratings[filtered_titles].sort_values().head(10)
st.dataframe(worst_movies)

# Análise: Filmes mais Avaliados
st.subheader("🎥 Filmes Mais Avaliados")
most_rated = count_ratings.sort_values(ascending=False).head(10)
st.bar_chart(most_rated)

# Análise: Distribuição de Avaliações
st.subheader("📊 Distribuição de Notas")
fig1, ax1 = plt.subplots()
sns.histplot(df['rating'], bins=10, ax=ax1)
ax1.set_xlabel("Nota")
ax1.set_ylabel("Frequência")
st.pyplot(fig1)

# Análise: Usuários mais ativos
st.subheader("👤 Top 10 Usuários que Mais Avaliaram")
user_counts = df['user_id'].value_counts().head(10)
st.bar_chart(user_counts)

# Análise: Relação entre média e número de avaliações
st.subheader("📈 Relação entre Média de Avaliação e Quantidade")
df_agg = df.groupby('title').agg({'rating': ['mean', 'count']})
df_agg.columns = ['media', 'quantidade']
fig2, ax2 = plt.subplots()
sns.scatterplot(data=df_agg, x='quantidade', y='media', ax=ax2)
st.pyplot(fig2)

# Análise: Filmes mais polarizados (variância)
st.subheader("⚡ Filmes Mais Polarizados")
variancia = df.groupby('title')['rating'].var()
polarizados = variancia[filtered_titles].sort_values(ascending=False).head(10)
st.dataframe(polarizados)

st.caption("Dashboard criado com Streamlit - Dados: MovieLens 100K")
