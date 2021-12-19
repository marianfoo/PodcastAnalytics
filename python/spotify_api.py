import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os


def get_all_episodes_show(show_id):
    client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv('SPOTIFY_CLIENT_ID'), client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'))
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    results = spotify.show_episodes(show_id, limit=50, market='DE')
    episodes = results['items']
    while results['next']:
        results = spotify.next(results)
        episodes.extend(results['items'])
    return episodes