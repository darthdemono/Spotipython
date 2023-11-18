# Spotipython
Getting Track and Album Data from Album link or, Using the search function using Spotify API through Python

### spotify_album.py:

  >Fetches information about a Spotify album and its tracks using the Spotify API.
  >Displays detailed information about the album, such as total tracks, album type, artist followers, genres, and additional details for each track.

### spotify_client.py:
  >Defines a SpotifyAPI class that handles authentication and makes requests to the Spotify API.
  >Provides methods to obtain an access token, fetch resources (like albums, artists, tracks), and perform searches.

### spotify_search.py:
  >Searches for tracks on Spotify based on user input (album, artist, explicit).
  >Retrieves information about the tracks, filters them based on explicit content, and prints detailed information about each track, including album details and external links.

### functions.py:
  >Contains utility functions used in other files.
  >Functions include converting milliseconds to minutes, formatting key-value pairs, converting explicit input to a boolean, extracting the last directory from a URL, and printing separator and space lines.
