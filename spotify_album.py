import os
from spotify_client import SpotifyAPI
from functions import ms_to_min, key_value, print_separator_line, print_space_line, get_last_directory
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)  # Set the desired logging level

def print_track_details(spotify, track_data, total_tracks):
    """
    Print details for a given track.

    Parameters:
    - spotify (SpotifyAPI): An instance of the SpotifyAPI class.
    - track_data (dict): The dictionary containing information about the track.
    - total_tracks (int): The total number of tracks in the album.
    """
    print_separator_line()
    track_id = track_data["id"]
    
    try:
        track_dict = spotify.get_resource("tracks", str(track_id))
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
        print("External IDs: ")
        for key, value in track_external_ids.items():
            print(f"    {key_value(key, value)}")
        print(f"Track Link: {track_link}")

    except KeyError as key_error:
        logging.error(f"KeyError while processing track: {key_error}")
    except Exception as err:
        logging.error(f"There was an error while processing track: {err}")

try:
    # Initialize Spotify API instance
    spotify = SpotifyAPI(os.getenv("client_id"), os.getenv("client_secret"))

    # Get user input for album URL
    album_link = input("Album URL:")
    album_id = get_last_directory(album_link)
    
    if not album_id:
        raise ValueError("Invalid album URL. Please provide a valid Spotify album URL.")

    # Retrieve album details from Spotify API
    album_dict = spotify.get_resource("albums", album_id)

    # Check for errors in the API response
    if not album_dict or "error" in album_dict:
        raise ValueError("Invalid album URL or the album does not exist. Please check your input.")

    # Extract relevant data directly from album_dict
    data = sorted(album_dict["tracks"]["items"], key=lambda x: (x["disc_number"], x["track_number"]))
    total_tracks = int(album_dict["total_tracks"])
    album_external_ids = album_dict["external_ids"]
    images = album_dict["images"][0]["url"]

    # Print basic information
    print_separator_line()
    print("ALBUM DATA:")
    print(f"Total Tracks: {total_tracks}")
    print(f"Album Type: {album_dict['album_type']}")
    print("External IDs:")
    for key, value in album_external_ids.items():
        print(f"    {key_value(key, value)}")
    # Print additional information
    for key in ["name", "release_date", "label"]:
        print(f"{key.title().replace('_', ' ')}: {album_dict[key]}")
    # Print the first "text" object from the copyright response
    copyright_text = album_dict.get("copyrights", [{"text": "Unknown"}])[0]["text"]
    print(f"Copyright: {copyright_text}")
    print(f"640px image: {images}")
    # Print artist details directly from the artist endpoint
    artist_id = album_dict["artists"][0]["id"]
    artist_dict = spotify.get_resource("artists", artist_id)
    followers = artist_dict["followers"]["total"]
    artist_genres = artist_dict["genres"] if artist_dict["genres"] else ["No genres have been given"]

    # Print artist details
    print_separator_line()
    print("ALBUM ARTIST DATA:")
    print(f"Artist: {artist_dict['name']}")
    print(f"Followers: {followers}")
    print("Genres:", ", ".join(artist_genres))

    # Print space line for better readability
    print_space_line()
    print("TRACK DATA:")

    # Print details for each track in the album
    for track_data in data:
        print_track_details(spotify, track_data, total_tracks)

except ValueError as value_err:
    logging.error(f"ValueError: {value_err}")
except Exception as general_err:
    # Handle unexpected errors
    logging.error(f"An unexpected error occurred: {general_err}")
