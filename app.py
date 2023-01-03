import pickle
import streamlit as st
import pandas as pd
import requests 
from PIL import Image
import base64

# função que retorna a imagem do filme do tmdb oelo id
def get_poster(movie_id):

    API_KEY = 'd2dee50252ec42a906562d4f3c43dfb0'
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US'

    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    path = "https://image.tmdb.org/t/p/w500" + poster_path
    return path 
     
# função que retorna os ids e url do poster das 5 recomendações
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

# configuraçã da pagina
st.set_page_config( page_title = 'Recommender system',
    page_icon = 'https://www.svgrepo.com/show/34896/movie.svg',
     layout = 'centered',
    initial_sidebar_state = 'expanded'
)

st.header(':white[Sistema de recomendação de filmes]')


# carregamento da lista de filmes e as similaridades
dict_movies = pickle.load(open("C:/Users/prpau/Downloads/Recomendacao/movies_list.pkl", 'rb'))
similarity = pickle.load(open("C:/Users/prpau/Downloads/Recomendacao/similarity.pkl", 'rb'))
movies_data = pd.DataFrame(dict_movies)

titles = list(movies_data['title'])
select_movie = st.sidebar.selectbox("**SELECIONAR FILME**", titles)
id = movies_data[movies_data['title'] == select_movie]['id'].values[0]

# mostra a imagem do poster do filme selecionado
image = get_poster(id)
st.sidebar.image(image)


# background da pagina


def add_bg_from_local(image_file):

    img = Image.open(image_file)
    img = img.copy()
    img.putalpha(50)
    img.save('background.png')

    with open('background.png', "rb") as image2:

       
        encoded_string = base64.b64encode(image2.read())

        

    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        
        background-position: right;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

name = 'images/background.jpg' 
add_bg_from_local(name)  



#def convertImage():
 #   img = Image.open(name)
  #  img = img.copy()
   # img.putalpha(180)
    #img.save('transparent.png')
    #return img

#icon = convertImage()


#def add_bg_from_url():

 #   st.markdown(
  #       f"""
   #      <style>
    #     .stApp {{
     #        background-image: url(data:image/{"png"};base64,{encoded_string.decode()}));
      #       background-size: 20%;
       #      background-repeat: no-repeat;
        #     background-position: right;
         #    background-attachment: fixed;
         #    background-color: str
             
         #}}
         #</style>
         #""",
         #unsafe_allow_html=True
     #)

#add_bg_from_url() 

# botão que retorna as recomendações com imagemdo poster de cada
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
