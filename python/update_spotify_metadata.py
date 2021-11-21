import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from pathlib import Path
import csv
import os


def update_data(show_id,filename_csv,filename_csv_other,special_episodes):
    client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv('SPOTIFY_CLIENT_ID'), client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'))
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    results = spotify.show_episodes(show_id, limit=50, market='DE')
    episodes = results['items']
    while results['next']:
        results = spotify.next(results)
        episodes.extend(results['items'])

    episodes_pd = []
    episodes_other = []
    for episode in episodes:
        desc = episode['description'].replace(' Learn more about your ad choices. Visit podcastchoices.com/adchoices', '')
        if any(episode['id'] in s for s in special_episodes):
            episodes_other.append([episode['id'],episode['release_date'],episode['external_urls']['spotify'],episode['name'],episode['duration_ms']/1000,desc])
        else:
            episodes_pd.append([episode['id'],episode['release_date'],episode['external_urls']['spotify'],episode['name'],episode['duration_ms']/1000,desc])
    
        
    df = pd.DataFrame(episodes_pd, columns = ['id', 'release_date','spotify_url', 'name','duration_sec','description'])
    df = df.sort_values(by=['release_date'], ascending=True)
    df = df.reset_index(drop=True)
    tracks = []
    for index, row in df.iterrows():
        tracks.append(index + 1)
    df['track'] = tracks
    df = df[['id','track','release_date','duration_sec','spotify_url','name','description']]
    print(df)
    print(str(Path().resolve().parent.resolve()) + '/PodcastAnalyticsF-F-S-S/data/' + filename_csv)
    df.to_csv(str(Path().resolve().parent.resolve()) + '/PodcastAnalyticsF-F-S-S/data/' + filename_csv, index = False, header=True)
    df.to_csv(str(Path().resolve().parent.resolve()) + '/PodcastAnalyticsF-F-S-S/docs/_data/' + filename_csv, index = False, header=True)

    if len(episodes_other) > 0 :
        df = pd.DataFrame(episodes_other, columns = ['id', 'release_date','spotify_url', 'name','duration_sec','description'])
        df = df.sort_values(by=['release_date'], ascending=True)
        df = df.reset_index(drop=True)
        tracks = []
        for index, row in df.iterrows():
            tracks.append(index + 1)
        df['track'] = tracks
        df = df[['id','track','release_date','duration_sec','spotify_url','name','description']]
        df.to_csv(str(Path().resolve().parent.resolve()) + '/PodcastAnalyticsF-F-S-S/data/' + filename_csv_other, index = False, header=True)
        df.to_csv(str(Path().resolve().parent.resolve()) + '/PodcastAnalyticsF-F-S-S/docs/_data/' + filename_csv_other, index = False, header=True)
    
def get_metadata(filename_csv):
    metadata = []
    with open(filename_csv, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            metadata.append(row)
    return metadata