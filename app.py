import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st

def authenticate_spotify():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id='20c8bdfc98024b9491ac6dfaae38c934',
        client_secret='2c7e2a64ffda4a73a623c0ab48f4ed4c',
        redirect_uri='http://localhost:8888/callbackv',
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
        
        # Search for tracks in batches to avoid slow loading
        total_tracks = 30
        track_ids = []
        for offset in range(0, total_tracks, 10):  # Adjust batch size if necessary
            results = sp.search(q=f'{mood} {genre}', limit=10, offset=offset, type='track')
            track_ids.extend([track['id'] for track in results['tracks']['items']])
        
        # Add tracks to the playlist
        if track_ids:
            sp.playlist_add_items(playlist_id=playlist['id'], items=track_ids[:total_tracks])
        
        st.success('Playlist created successfully!')
        st.write(f'Playlist Name: {playlist_name}')
        st.write('Tracks added:')
        for track_id in track_ids[:total_tracks]:  # Ensure only up to total_tracks are listed
            track = sp.track(track_id)
            st.write(track['name'])
