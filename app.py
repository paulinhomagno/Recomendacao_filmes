import pickle
#import sys
#sys.path.append("/opt/anaconda3/lib/python3.9/site-packages")

import streamlit as st
import pandas as pd
import requests 

def get_poster(movie_id):

    API_KEY = 'd2dee50252ec42a906562d4f3c43dfb0'
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US'

    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    path = "https://image.tmdb.org/t/p/w500" + poster_path
    return path 
     

def rec_function(movie):

    idx = movies_data[movies_data['title'] == movie].index[0]
    
    distance = sorted(list(enumerate(similarity[idx])), reverse = True, key = lambda x:x[1]) 
    
    name_movies_rec = []

    poster_movies_rec = []

    for i in distance[1:6]:

        movie_id = movies_data.iloc[i[0]].id
        poster_movies_rec.append(get_poster(movie_id))
        name_movies_rec.append(movies_data.iloc[i[0]].title)

    return name_movies_rec, poster_movies_rec


st.header('Sistema de recomendação de filmes')

dict_movies = pickle.load(open("C:/Users/prpau/Downloads/Recomendacao/movies_list.pkl", 'rb'))
similarity = pickle.load(open("C:/Users/prpau/Downloads/Recomendacao/similarity.pkl", 'rb'))
movies_data = pd.DataFrame(dict_movies)

titles = list(movies_data['title'])
select_movie = st.selectbox("Selecionar filme", titles)

if st.button("Mostrar recomendações"):

    name_movies_rec, poster_movies_rec = rec_function(select_movie)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(name_movies_rec[0])
        st.image(poster_movies_rec[0])

    with col2:
        st.text(name_movies_rec[1])
        st.image(poster_movies_rec[1])

    with col3:
        st.text(name_movies_rec[2])
        st.image(poster_movies_rec[2])

    with col4:
        st.text(name_movies_rec[3])
        st.image(poster_movies_rec[3])

    with col5:
        st.text(name_movies_rec[4])
        st.image(poster_movies_rec[4])
