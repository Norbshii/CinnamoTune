import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = 'user-library-read'
client_id = '20c8bdfc98024b9491ac6dfaae38c934'
client_secret = '2c7e2a64ffda4a73a623c0ab48f4ed4c'
redirect_uri = 'http://localhost:8501/callback'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                                              redirect_uri=redirect_uri, scope=scope))

def fetch_songs(mood, activity, energy):
    # Define the search query based on user input
    query = f"{mood} {activity}"
    if energy:
        query += " energetic"
    
    # Search tracks based on the query
    results = sp.search(q=query, limit=10, type='track')
    tracks = results['tracks']['items']
    return tracks

# Streamlit interface
st.title('Spotify Song Suggester')
st.header('Tell us how you feel and what you want to listen to!')

mood = st.selectbox('How are you feeling?', ['Happy', 'Sad', 'Energetic', 'Calm', 'Angry', 'Romantic'])
activity = st.selectbox('What are you planning to do?', ['Study', 'Workout', 'Relax', 'Party', 'Read'])
energy = st.checkbox('Do you want to feel powerful?')

if st.button('Suggest Songs'):
    songs = fetch_songs(mood, activity, energy)
    if songs:
        st.subheader('Songs that might suit your mood:')
        for song in songs:
            st.write(f"**{song['name']}** by {', '.join(artist['name'] for artist in song['artists'])}")
    else:
        st.write("No songs found. Try different settings!")

