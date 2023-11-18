import os
from spotify_client import *
from functions import *
from dotenv import load_dotenv
import json
load_dotenv()

spotify = SpotifyAPI(os.getenv("client_id"), os.getenv("client_secret"))

album = input("Album: ")
artist = input("Artist: ")
explicit = explicit_to_boolean()

track_dict = spotify.search({"album": album,"artist": artist},search_type="track")

data = track_dict["tracks"]["items"]
data.sort(key=lambda x: (x["disc_number"], x["track_number"]))

total_tracks = int(data[0]["album"]["total_tracks"])
album_id = data[0]["album"]["id"]
artist_id = data[0]["artists"][0]["id"]
album_type = data[0]["album"]["album_type"]

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, sort_keys=True, ensure_ascii=True, indent=2)

artist_dict = spotify.get_resource("artists", f"{artist_id}")
followers = artist_dict["followers"]["total"]
artist_genres = artist_dict["genres"]

print("_______________________________________________________________________")
print(f"Total Tracks: {total_tracks}")
print(f"Album Type: {album_type}")
print(f"Artist Followers: {followers}")
for genre in artist_genres:
    print(f"Artist Genres: {genre}")

filtered_data = [item for item in data if item["explicit"] == explicit]

for i, item in enumerate(filtered_data):
    try:
        print("_______________________________________________________________________")
        track_explicit = item["explicit"]
        track_number = int(item["track_number"])
        disc_number = int(item["disc_number"])
        track_name = item["name"]
        track_duration_ms = item["duration_ms"]
        track_duration = ms_to_min(track_duration_ms)
        album_type = item["album"]["album_type"]
        track_external_ids = item["external_ids"]
        release_date = item["album"]["release_date"]
        track_link = item["external_urls"]["spotify"]
        album_link = item["album"]["external_urls"]["spotify"]
        artist_link = item["album"]["artists"][0]["external_urls"]["spotify"]
        images = item["album"]["images"][0]["url"]
        album_id = item["album"]["id"]
        album_dict = spotify.get_resource("albums", f"{album_id}")
        copyrights = album_dict["copyrights"][0]["text"]
        album_external_ids = album_dict["external_ids"]
        label = album_dict["label"]
        artists = item["artists"]
        track_artists = '; '.join(artist["name"] for artist in artists)
        print(f"For Track Number {track_number}/{total_tracks}:")
        print(f"Disc Number: {disc_number}")
        print(f"Track Name: {track_name}")
        print(f"Track Artists: {track_artists}")
        print(f"Track Duration: {track_duration}")
        print(f"Album Type: {album_type}")
        print(f"Track Explicit: {track_explicit}")
        print("External IDs: ")
        for key, value in track_external_ids.items():
            print(f"    {key_value(key, value)}")
        for key, value in album_external_ids.items():
            print(f"    {key_value(key, value)}")
        print(f"Release Date: {release_date}")
        print(f"Copyrights: {copyrights}")
        print(f"Label: {label}")
        print(f"Track Link: {track_link}")
        print(f"Album link: {album_link}")
        print(f"Artist Link: {artist_link}")
        print(f"640px image: {images}")
    except Exception as err:
        print(f"There Was an Error :{err}")