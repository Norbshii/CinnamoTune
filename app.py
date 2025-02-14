import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st

def authenticate_spotify():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id='YOUR_CLIENT_ID',
        client_secret='YOUR_CLIENT_SECRET',
        redirect_uri='http://localhost:8501/callback',
        scope="playlist-modify-public user-read-private"))
    return sp
st.title('Spotify Playlist Generator')

# User inputs
mood = st.selectbox('What is your mood?', ['Happy', 'Sad', 'Energetic', 'Calm'])
genre = st.selectbox('Select your favorite genre', ['Pop', 'Rock', 'Jazz', 'Classical'])
playlist_name = st.text_input('Name your playlist', value=f'{mood} {genre} Vibes')

if st.button('Generate Playlist'):
    sp = authenticate_spotify()
    if sp:
        user_id = sp.current_user()['id']  # Get the user's Spotify ID
        playlist = sp.user_playlist_create(user_id, playlist_name, public=True)  # Create a new playlist
        results = sp.search(q=f'{mood} {genre}', limit=10, type='track')
        track_ids = [track['id'] for track in results['tracks']['items']]
        sp.playlist_add_items(playlist_id=playlist['id'], items=track_ids)
        st.success('Playlist created successfully!')
        st.write(f'Playlist Name: {playlist_name}')
        st.write('Tracks added:')
        for track in results['tracks']['items']:
            st.write(track['name'])
