import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Setup the authentication
client_id = '20c8bdfc98024b9491ac6dfaae38c934'
client_secret = '2c7e2a64ffda4a73a623c0ab48f4ed4c'
redirect_uri = 'http://localhost:8080/callback'
scope = 'playlist-modify-public'

# Initialize Spotipy with SpotifyOAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id,
                                               client_secret=client_secret, redirect_uri=redirect_uri))

def create_playlist(name, description):
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user_id, name, public=True, description=description)
    return playlist

# Streamlit interface
st.title('Spotify Playlist Creator')
playlist_name = st.text_input('Enter playlist name:')
playlist_description = st.text_area('Enter playlist description:')

if st.button('Create Playlist'):
    result = create_playlist(playlist_name, playlist_description)
    if result:
        st.success('Playlist created successfully!')
        st.write('Playlist ID:', result['id'])
    else:
        st.error('Failed to create playlist.')

