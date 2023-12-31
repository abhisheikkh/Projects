import streamlit as st
import pickle
import pandas as pd
import requests

# Fetch API key from secrets
tmdb_api_key = st.secrets["tmdb_api_key"]

# Load paths from secrets
model_pickle_path = st.secrets["model_pickle_path"]
similarity_pickle_path = st.secrets["similarity_pickle_path"]

# Load your pickled files
movies_dict = pickle.load(open(model_pickle_path, 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open(similarity_pickle_path, 'rb'))

def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_api_key}&language=en-US'
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

st.title('Movie-Recommender-System')
selected_movie_name = st.selectbox(
    'Select a movie to recommend',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3 = st.columns(3)

    # First row
    with col1:
        st.text(names[0])
        st.image(posters[0], use_column_width=True, width=100)

    with col2:
        st.text(names[1])
        st.image(posters[1], use_column_width=True, width=100)

    with col3:
        st.text(names[2])
        st.image(posters[2], use_column_width=True, width=100)

    # Second row
    col4, col5 = st.columns(2)

    with col4:
        st.text(names[3])
        st.image(posters[3], use_column_width=True, width=100)

    with col5:
        st.text(names[4])
        st.image(posters[4], use_column_width=True, width=100)

# Apply custom CSS for font
st.markdown(
    """
    <style>
        .stText {
            font-family: 'Verdana', sans-serif;
        }
    </style>
    """,
    unsafe_allow_html=True
)
