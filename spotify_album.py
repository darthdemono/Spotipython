import os
from spotify_client import *
from functions import *
from dotenv import load_dotenv
load_dotenv()

spotify = SpotifyAPI(os.getenv("client_id"), os.getenv("client_secret"))

album_link = input("Album URL:")
album_id = get_last_directory(album_link)
album_dict = spotify.get_resource("albums", album_id)

# Extract relevant data directly from album_dict
data = sorted(album_dict["tracks"]["items"], key=lambda x: (x["disc_number"], x["track_number"]))
album_type = album_dict["album_type"]
album_name = album_dict["name"]
release_date = album_dict["release_date"]
album_artist = album_dict["artists"][0]["name"]
artist_id = album_dict["artists"][0]["id"]
artist_link = album_dict["artists"][0]["external_urls"]["spotify"]
copyrights = album_dict["copyrights"][0]["text"]
album_external_ids = album_dict["external_ids"]
label = album_dict["label"]
total_tracks = int(album_dict["total_tracks"])

# Fetch artist details directly from the artist endpoint
artist_dict = spotify.get_resource("artists", artist_id)
followers = artist_dict["followers"]["total"]
artist_genres = artist_dict["genres"]
album_image_640px = album_dict["images"][0]["url"]

# Print basic information
print_separator_line()
print("ALBUM DATA:")
print(f"Total Tracks: {total_tracks}")
print(f"Album Type: {album_type}")
print(f"Artist Followers: {followers}")

# Print artist genres
print("Artist Genres:", ", ".join(artist_genres))

# Print external album IDs
print("External Album IDs: ")
for key, value in album_external_ids.items():
    print(f"    {key_value(key, value)}")

# Print additional information
for key in ["Release Date", "Copyrights", "Label", "Album link", "Artist Link", "Album image 640px"]:
    print(f"{key}: {locals()[key.lower().replace(' ', '_')]}")

print_space_line
print("TRACK DATA:")

for i, track_data in enumerate(data):
    try:
        print_separator_line()
        track_id = track_data["id"]
        track_dict = spotify.get_resource("tracks", str(track_id))
        track_explicit = track_dict["explicit"]
        track_number = int(track_dict["track_number"])
        disc_number = int(track_dict["disc_number"])
        track_name = track_dict["name"]
        track_duration_ms = track_dict["duration_ms"]
        track_duration = ms_to_min(track_duration_ms)
        track_external_ids = track_dict["external_ids"]
        track_link = track_dict["external_urls"]["spotify"]
        artists = track_dict["artists"]
        track_artists = '; '.join(artist["name"] for artist in artists)

        print(f"{track_number}. {track_name} - {track_artists} ({track_duration})")
        print(f"For Track Number {track_number}/{total_tracks}:")
        print(f"Disc Number: {disc_number}")
        print(f"Track Name: {track_name}")
        print(f"Track Artists: {track_artists}")
        print(f"Track Duration: {track_duration}")
        print(f"Track Explicit: {track_explicit}")
        print("External IDs: ")
        for key, value in track_external_ids.items():
            print(f"    {key_value(key, value)}")
        print(f"Track Link: {track_link}")
    except Exception as err:
        print(f"There Was an Error :{err}")

