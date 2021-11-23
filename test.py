import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='streaming user-modify-playback-state', redirect_uri='https://google.com'))
spotify.pause_playback()
