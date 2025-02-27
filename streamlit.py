import streamlit as st
import pickle

# Load data
movies = pickle.load(open("movies_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# Convert to a list and limit to 10,000 movies
movies_list = movies['title'].astype(str).tolist()[:10000]

# Streamlit Header
st.markdown("<h1 style='color: #FF4B4B;'>Movie Recommender System By Sreekethana</h1>", unsafe_allow_html=True)

# Movie selection dropdown (limited to 10,000 movies)
selected_movie = st.selectbox("Select a movie", movies_list)

# Function to fetch recommendations
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index
    if movie_index.empty:
        st.error(f"The movie '{movie}' does not exist in the dataset.")
        return []

    movie_index = movie_index[0]

    if movie_index >= len(similarity):
        st.error(f"Error: The movie '{movie}' is not within the bounds of the similarity matrix.")
        return []

    similarity_scores = similarity[movie_index]

    # Sort movies based on similarity scores
    distance = sorted(enumerate(similarity_scores), reverse=True, key=lambda vector: vector[1])

    recommended_movies = []
    for i in distance[1:6]:  
        if i[0] < len(movies):  # Prevent index errors
            movie_data = movies.iloc[i[0]]
            recommended_movies.append({
                "title": movie_data.title,
                "poster": movie_data.poster_path if 'poster_path' in movie_data else None
            })

    return recommended_movies

# Button to show recommendations
if st.button("Show Recommendations"):
    recommended_movies = recommend(selected_movie)

    if recommended_movies:
        cols = st.columns(5)  
        for idx, movie in enumerate(recommended_movies):
            with cols[idx]:  
                st.markdown(f"<h3 style='text-align: center; color: #4B9CD3;'>{movie['title']}</h3>", unsafe_allow_html=True)
                if movie["poster"]:
                    st.image(f"https://image.tmdb.org/t/p/w500{movie['poster']}", use_column_width=True)
                else:
                    st.write("No Image Available")
    else:
        st.write("Not enough recommendations available.")
