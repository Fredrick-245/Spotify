import requests
import html
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import smtplib

from bs4 import BeautifulSoup

SPOTIFY_CLIENT_ID = "c519a21652214990aeede5fec7337db0"
SPOTIFY_CLIENT_SECRET = "a06478e9b3b744d8beb47dd18da6a300"
SPOTIFY_REDIRECT = "http://example.com"
my_password="ljtlxqizmyodbtlz"
my_email="ndemofredrick245@gmail.com"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT,
    scope="playlist-modify-private",
    show_dialog=True,
    cache_path="token.txt"
))
user_id = sp.current_user()["id"]

date = input('What is the date you want to go back to😊:YYYY-MM-DD: ')

billboard_endpoint = f"https://www.billboard.com/charts/hot-100/{date}"
response = requests.get(billboard_endpoint)

billboard_html = response.text
soup = BeautifulSoup(billboard_html, 'html.parser')
top_100_songs =[html.escape(song.text).strip() for song in soup.select("li ul li h3")]

# print(top_100_songs)
song_uris = []

year = date.split('-')[0]
for song in top_100_songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri=result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in spotify.Skipped")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

with smtplib.SMTP('smtp.gmail.com') as connection:
    connection.starttls()
    connection.login(user=my_email,password=my_password)
    connection.sendmail(from_addr=my_email,to_addrs=my_email,msg=f"Subject:Playlist added\n\nYou just added {date} Billboard 100 as a new playlist.Have fun listening to the songs ")
