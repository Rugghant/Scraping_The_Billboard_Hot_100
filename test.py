from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

# Scraping Billboard 100
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")
year = date.split("-")[0]
URL = f"https://www.billboard.com/charts/hot-100/{year}"
response = requests.get(URL)
website_html = response.text
soup = BeautifulSoup(website_html, "html.parser")
song_tags = soup.select(selector="li ul li h3")
song_titles = [song_tag.getText().strip() for song_tag in song_tags]
# print(song_titles)

client_id = "d210939c4e594a24947961285a4ca32d"
client_secret = "737d4b8e85d840b7994118681b0907c8"
redirect_uri = "http://example.com"
scope = "playlist-modify-private"
sp = spotipy.Spotify(
  auth_manager=SpotifyOAuth(
      client_id=client_id,
      client_secret=client_secret,
      redirect_uri=redirect_uri,
      scope=scope,
      cache_path="token.txt",
      show_dialog=True,
    )
)
results = sp.current_user()
user_id = results["id"]
# print(user_id)

# Search Spotify For The Songs
songs_uris = []
for song in song_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # pprint(result["tracks"]["items"][0]["uri"])
    try:
        uri = result["tracks"]["items"][0]["uri"]
        songs_uris.append(uri)
    except IndexError:
        print(f"{song}doesn't exists in spotify. skipped.")

# Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)
# Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=songs_uris)
