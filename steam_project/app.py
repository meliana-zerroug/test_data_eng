import streamlit as st
import pymongo
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Steam Games Explorer", page_icon="🎮", layout="wide")

# MongoDB connexion 
@st.cache_resource
def get_database():
    client = pymongo.MongoClient('mongodb://mongodb:27017/')
    return client['projet']['steam_games']

collection = get_database()

# Titre principal
st.title("🎮 Steam Games Explorer")
st.markdown("---")

st.sidebar.header("🔍 Filtres")

# Statistiques générales
col1, col2, col3 = st.columns(3)

with col1:
    total_games = collection.count_documents({})
    st.metric("🎯 Total de jeux", total_games)

with col2:
    free_games = collection.count_documents({"price": "Gratuit"})
    st.metric("🆓 Jeux gratuits", free_games)

with col3:
    paid_games = total_games - free_games
    st.metric("💰 Jeux payants", paid_games)

st.markdown("---")

# Récupérer toutes les données
@st.cache_data
def load_data():
    data = list(collection.find({}, {'_id': 0}))
    df = pd.DataFrame(data)
    # Vérifier que la colonne price existe, sinon ajouter une valeur par défaut
    if 'price' not in df.columns:
        df['price'] = 'N/A'
    return df

df = load_data()

# Onglets
tab1, tab2, tab3 = st.tabs([" Visualisations", "🔎 Recherche", " Données brutes"])

with tab1:
    st.header("📊 Statistiques et graphiques")
    
    # Top 10 tags
    if 'tags' in df.columns:
        st.subheader(" Top 10 des tags")
        tags_list = []
        for tags in df['tags'].dropna():
            if isinstance(tags, str):
                tags_list.extend([tag.strip() for tag in tags.split(',')])
        
        if tags_list:
            tags_df = pd.DataFrame({'tag': tags_list})
            top_tags = tags_df['tag'].value_counts().head(10)
            fig = px.bar(x=top_tags.values, y=top_tags.index, orientation='h',
                        labels={'x': 'Nombre de jeux', 'y': 'Tag'},
                        title="Top 10 des tags les plus populaires")
            st.plotly_chart(fig, use_container_width=True)
    
    # Distribution des prix
    st.subheader(" Distribution des prix")
    if not df.empty and 'price' in df.columns and len(df['price'].dropna()) > 0:
        price_counts = df['price'].value_counts().head(10)
        fig2 = px.pie(values=price_counts.values, names=price_counts.index,
                      title="Répartition des prix (Top 10)")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Pas de données de prix disponibles")

with tab2:
    st.header("🔎 Moteur de recherche")
    
    search_term = st.text_input(" Rechercher un jeu par titre", "")
    
    if search_term:
        results = collection.find(
            {"title": {"$regex": search_term, "$options": "i"}},
            {'_id': 0}
        ).limit(20)
        
        results_list = list(results)
        
        if results_list:
            st.success(f" {len(results_list)} jeu(x) trouvé(s)")
            
            for game in results_list:
                with st.expander(f" {game.get('title', 'N/A')}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**💰 Prix:** {game.get('price', 'N/A')}")
                        st.write(f"**⭐ Avis:** {game.get('review', 'N/A')}")
                    with col2:
                        st.write(f"**📅 Date:** {game.get('date', 'N/A')}")
                        st.write(f"**Tags:** {game.get('tags', 'N/A')}")
        else:
            st.warning("❌ Aucun jeu trouvé")
    else:
        st.info(" Entrez un terme de recherche pour commencer")

with tab3:
    st.header(" Tableau de données")
    st.dataframe(df, use_container_width=True, height=500)
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=" Télécharger les données (CSV)",
        data=csv,
        file_name='steam_games.csv',
        mime='text/csv',
    )

st.markdown("---")
st.markdown("**🎮 Steam Games Data Engineering Project")