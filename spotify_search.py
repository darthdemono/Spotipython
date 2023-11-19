import os
import json
from spotify_client import SpotifyAPI
from functions import ms_to_min, key_value, explicit_to_boolean, print_separator_line
from dotenv import load_dotenv

load_dotenv()

spotify = SpotifyAPI(os.getenv("client_id"), os.getenv("client_secret"))

def print_track_details(item, total_tracks):
    """Print details for a track."""
    print("_______________________________________________________________________")
    # Extract relevant information from the track item
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

    # Print the extracted information
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

def print_artist_details(artist_id):
    """Print details for an artist."""
    print_separator_line()
    artist_dict = spotify.get_resource("artists", artist_id)
    followers = artist_dict["followers"]["total"]
    artist_genres = artist_dict["genres"]
    print(f"Total Tracks: {total_tracks}")
    print(f"Album Type: {album_type}")
    print(f"Artist Followers: {followers}")
    for genre in artist_genres:
        print(f"Artist Genres: {genre}")

try:
    # Get user input for album, artist, and explicit filter
    album = input("Album: ")
    artist = input("Artist: ")
    explicit = explicit_to_boolean()

    # Search for tracks based on user input
    track_dict = spotify.search({"album": album, "artist": artist}, search_type="track")
    data = track_dict["tracks"]["items"]

    if not data:
        print_separator_line()
        print("No tracks found for the given query.")
    else:
        # Sort tracks based on disc number and track number
        data.sort(key=lambda x: (x["disc_number"], x["track_number"]))
        total_tracks = int(data[0]["album"]["total_tracks"])
        album_type = data[0]["album"]["album_type"]
        # Filter tracks based on explicit filter
        filtered_data = [item for item in data if item["explicit"] == explicit]

        if not filtered_data:
            print_separator_line()
            print("No explicit tracks found for the given query.")
        else:
            # Print details for the first artist (assuming all tracks have the same artist)
            print_artist_details(data[0]['artists'][0]['id'])
            # Print details for each filtered track
            for item in filtered_data:
                try:
                    print_track_details(item, total_tracks)
                except KeyError as key_error:
                    print(f"Error processing track: {key_error}")
                except Exception as err:
                    print(f"An error occurred while processing track: {err}")

except Exception as general_err:
    print(f"An unexpected error occurred: {general_err}")
