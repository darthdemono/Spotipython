# Import statements
import os
import logging
import base64
import datetime
import time
from urllib.parse import urlparse, urlencode
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Set up logging
logging.basicConfig(level=logging.INFO)

class Function:
    def get_last_directory(url):
        """Extract the last segment of a URL path."""
        path = urlparse(url).path.rstrip('/')
        return path.split('/')[-1]
    def ms_to_min(ms):
        """Convert milliseconds to a formatted string representing minutes and seconds."""
        seconds, millis = divmod(int(ms), 1000)
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes}:{seconds:02d}"
    def key_value(key, value):
        """Format key-value pair as an uppercase string."""
        return f"{key.upper()}: {value.upper()}"
    def explicit_to_boolean():
        """Get user input for track explicitness and convert it to a boolean value."""
        explicit = input("Track Explicit: ")
        return explicit.lower() == "true"
    def print_separator_line():
        """Print a separator line for better output formatting."""
        print("_______________________________________________________________________")
    def print_space_line():
        """Print an empty line for better output readability."""
        print("                                                                       ")

# Class definitions
class SpotifyAPI:
    TOKEN_URL = "https://accounts.spotify.com/api/token"
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.access_token_expires = datetime.datetime.now()
        self.access_token_did_expire = True

    def get_client_credentials(self):
        if not all([self.client_id, self.client_secret]):
            raise ValueError("You must set client_id and client_secret")
        client_creds = f"{self.client_id}:{self.client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode()).decode()
        return client_creds_b64

    def get_token_headers(self):
        return {"Authorization": f"Basic {self.get_client_credentials()}"}

    def get_token_data(self):
        return {"grant_type": "client_credentials"}

    def perform_auth(self):
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        response = requests.post(self.TOKEN_URL, data=token_data, headers=token_headers)

        if response.status_code not in range(200, 299):
            raise ValueError(f"Authentication failed. Status code: {response.status_code}")

        data = response.json()
        access_token = data.get('access_token')
        expires_in = data.get('expires_in', 0)
        expires = datetime.datetime.now() + datetime.timedelta(seconds=expires_in)

        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < datetime.datetime.now()
        return True

    def get_access_token(self):
        if self.access_token_did_expire or self.access_token is None:
            self.perform_auth()
        return self.access_token

    def get_resource_header(self):
        return {"Authorization": f"Bearer {self.get_access_token()}"}

    def get_resource(self, resource_type, lookup_id, params=None, headers=None):
        endpoint = f"https://api.spotify.com/v1/{resource_type}/{lookup_id}"
        headers = headers or self.get_resource_header()
        return self._make_request(endpoint, headers, params=params)

    def base_search(self, query_params):
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        lookup_url = f"{endpoint}?{query_params}&limit=40"
        return self._make_request(lookup_url, headers)

    def _make_request(self, url, headers, params=None):
        max_retries = 3
        retries = 0

        while retries < max_retries:
            try:
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()  # Raise an error for HTTP errors (4xx, 5xx)
                return response.json()
            except requests.exceptions.HTTPError as http_err:
                if response.status_code == 429:  # Rate Limit Exceeded
                    retry_after = int(response.headers.get('Retry-After', 5))  # Default to 5 seconds
                    logging.info(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
                    time.sleep(retry_after)
                    retries += 1
                elif response.status_code == 400:  # Client Error (Bad Request)
                    error_message = response.json().get('error', {}).get('message', 'Unknown Error')
                    raise ValueError(f"HTTP error occurred: {response.status_code} Client Error: {error_message} for url: {url}")
                else:
                    logging.error(f"HTTP error occurred: {http_err}. Response: {response.text}")
                    raise
            except Exception as err:
                logging.error(f"An unexpected error occurred: {err}")
                raise

        logging.error(f"Reached max retries. Aborting request.")
        raise ValueError("Reached max retries.")
    
    def search(self, query=None, operator=None, operator_query=None, search_type='artist'):
        """
        Search for tracks, albums, or artists on Spotify.
        """
        if query is None:
            raise ValueError("A query is required")

        if isinstance(query, dict):
            query = " ".join([f"{k}:{v}" for k, v in query.items()])

        if operator and operator_query and operator.lower() in ["or", "not"]:
            operator = operator.upper()
            if isinstance(operator_query, str):
                query = f"{query} {operator} {operator_query}"

        query_params = urlencode({"q": query, "type": search_type.lower()})
        return self.base_search(query_params)

class Album:
    def print_track_details(spotify, track_data, total_tracks):
        """
        Print details for a given track.

        Parameters:
        - spotify (SpotifyAPI): An instance of the SpotifyAPI class.
        - track_data (dict): The dictionary containing information about the track.
        - total_tracks (int): The total number of tracks in the album.
        """
        Function.print_separator_line()
        track_id = track_data["id"]
        
        try:
            track_dict = spotify.get_resource("tracks", str(track_id))
            track_number = int(track_dict["track_number"])
            disc_number = int(track_dict["disc_number"])
            track_name = track_dict["name"]
            track_duration_ms = track_dict["duration_ms"]
            track_duration = Function.ms_to_min(track_duration_ms)
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
                print(f"    {Function.key_value(key, value)}")
            print(f"Track Link: {track_link}")

        except KeyError as key_error:
            logging.error(f"KeyError while processing track: {key_error}")
        except Exception as err:
            logging.error(f"There was an error while processing track: {err}")


class Search:
    def print_track_details(item, total_tracks):
        """Print details for a track."""
        print("_______________________________________________________________________")
        # Extract relevant information from the track item
        track_explicit = item["explicit"]
        track_number = int(item["track_number"])
        disc_number = int(item["disc_number"])
        track_name = item["name"]
        track_duration_ms = item["duration_ms"]
        track_duration = Function.ms_to_min(track_duration_ms)
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
            print(f"    {Function.key_value(key, value)}")
        for key, value in album_external_ids.items():
            print(f"    {Function.key_value(key, value)}")
        print(f"Release Date: {release_date}")
        print(f"Copyrights: {copyrights}")
        print(f"Label: {label}")
        print(f"Track Link: {track_link}")
        print(f"Album link: {album_link}")
        print(f"Artist Link: {artist_link}")
        print(f"640px image: {images}")

    def print_artist_details(artist_id):
        """Print details for an artist."""
        Function.print_separator_line()
        artist_dict = spotify.get_resource("artists", artist_id)
        followers = artist_dict["followers"]["total"]
        artist_genres = artist_dict["genres"]
        print(f"Total Tracks: {total_tracks}")
        print(f"Album Type: {album_type}")
        print(f"Artist Followers: {followers}")
        for genre in artist_genres:
            print(f"Artist Genres: {genre}")

# Main execution logic
if __name__ == "__main__":
    print("Do you want to Search or Input Album?")
    print("Type 1 for Search")
    print("Type 2 for Album Link")
    soi = input("Input: ")

    if soi == "1":
        try:
            spotify = SpotifyAPI(os.getenv("client_id"), os.getenv("client_secret"))
            # Get user input for album, artist, and explicit filter
            album = input("Album: ")
            artist = input("Artist: ")
            explicit = Function.explicit_to_boolean()

            # Search for tracks based on user input
            track_dict = spotify.search({"album": album, "artist": artist}, search_type="track")
            data = track_dict["tracks"]["items"]

            if not data:
                Function.print_separator_line()
                print("No tracks found for the given query.")
            else:
                # Sort tracks based on disc number and track number
                data.sort(key=lambda x: (x["disc_number"], x["track_number"]))
                total_tracks = int(data[0]["album"]["total_tracks"])
                album_type = data[0]["album"]["album_type"]
                # Filter tracks based on explicit filter
                filtered_data = [item for item in data if item["explicit"] == explicit]

                if not filtered_data:
                    Function.print_separator_line()
                    print("No explicit tracks found for the given query.")
                else:
                    # Print details for the first artist (assuming all tracks have the same artist)
                    Search.print_artist_details(data[0]['artists'][0]['id'])
                    # Print details for each filtered track
                    for item in filtered_data:
                        try:
                            Search.print_track_details(item, total_tracks)
                        except KeyError as key_error:
                            print(f"Error processing track: {key_error}")
                        except Exception as err:
                            print(f"An error occurred while processing track: {err}")
        except Exception as general_err:
            print(f"An unexpected error occurred: {general_err}")

    elif soi == "2":
        try:
            # Initialize Spotify API instance
            spotify = SpotifyAPI(os.getenv("client_id"), os.getenv("client_secret"))

            # Get user input for album URL
            album_link = input("Album URL:")
            album_id = Function.get_last_directory(album_link)
            
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
            Function.print_separator_line()
            print("ALBUM DATA:")
            print(f"Total Tracks: {total_tracks}")
            print(f"Album Type: {album_dict['album_type']}")
            print("External IDs:")
            for key, value in album_external_ids.items():
                print(f"    {Function.key_value(key, value)}")
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
            Function.print_separator_line()
            print("ALBUM ARTIST DATA:")
            print(f"Artist: {artist_dict['name']}")
            print(f"Followers: {followers}")
            print("Genres:", ", ".join(artist_genres))

            # Print space line for better readability
            Function.print_space_line()
            print("TRACK DATA:")

            # Print details for each track in the album
            for track_data in data:
                Album.print_track_details(spotify, track_data, total_tracks)
        except ValueError as value_err:
            logging.error(f"ValueError: {value_err}")
        except Exception as general_err:
            # Handle unexpected errors
            logging.error(f"An unexpected error occurred: {general_err}")
    else:
        print("Wrong input")
