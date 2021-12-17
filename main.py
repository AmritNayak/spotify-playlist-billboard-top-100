from pprint import pprint
from bs4 import BeautifulSoup
import requests as req
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

client = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri='https://example.com',
        scope='playlist-modify-public',
        cache_path='.cache'
    )
)

user_id = client.current_user()['id']

date = input("What year do you want to travel to ? Type the date in this format YYYY-MM-DD: ")
# date = '2021-12-17'
URL = f"https://www.billboard.com/charts/hot-100/{date}"

soup = BeautifulSoup(req.get(URL).text, "html.parser")
song_names = [song.getText().strip() for song in soup.select(selector='li h3.c-title')]
# pprint(song_names)

song_uris = []
for song in song_names:
    res = client.search(q=f'track:{song} year:{date.split("-")[0]}', type='track')
    try:
        uri = res['tracks']['items'][0]['uri']
        song_uris.append(uri)
    except IndexError:
        # pprint(res['tracks'])
        print(f'{song} not available on Spotify.')

# print(song_uris)
print(len(song_uris))
playlist = client.user_playlist_create(user=user_id, name=f'Billboard Top {date}', public=True)
# print(playlist)

client.playlist_add_items(playlist_id=playlist['id'], items=song_uris)
print('Playlist added!')
