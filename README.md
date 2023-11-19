<div align="center">
  <img src="https://miro.medium.com/v2/resize:fit:1200/0*eIfW4F5Q4ZQs6X99" width="500" align="center">
  <h1>Spotipython</h1>
  
  <p align="center">
  <i>An open-source project for fetching Spotify track and album data programmatically using Python and the Spotify API.</i>
  </p>
  
  [![Badge](https://img.shields.io/github/issues/darthdemono/Spotipython?style=for-the-badge)](https://github.com/darthdemono/Spotipython/issues)
  [![Badge](https://img.shields.io/github/forks/darthdemono/Spotipython?style=for-the-badge)](https://github.com/darthdemono/Spotipython/network)
  [![Badge](https://img.shields.io/github/stars/darthdemono/Spotipython?style=for-the-badge)](https://github.com/darthdemono/Spotipython/stargazers)
</div>


## Introduction
Spotipython is a Python project that utilizes the Spotify API to fetch detailed information about albums, artists, and tracks. Whether you have an album link or want to search for specific tracks, Spotipython provides scripts to gather the data you need programmatically.

## Scripts
### spotify_album.py
- Fetches information about a Spotify album and its tracks.
- Displays detailed information about the album, such as total tracks, album type, artist followers, genres, and additional details for each track.
- **Inputs:** Album Link

### spotify_search.py
- Searches for tracks on Spotify based on user input (album, artist, explicit).
- Retrieves information about the tracks, filters them based on explicit content, and prints detailed information about each track, including album details and external links.
- **Inputs:** Album Name, Artist Name, Explicit (True or, False)

### spotify_client.py
- Defines a SpotifyAPI class that handles authentication and makes requests to the Spotify API.
- Provides methods to obtain an access token, fetch resources (like albums, artists, tracks), and perform searches.

### functions.py
- Contains utility functions used in other files.
- Functions include converting milliseconds to minutes, formatting key-value pairs, converting explicit input to a boolean, extracting the last directory from a URL, and printing separator and space lines.

### Dotenv
- Dotenv file contains your "client_id" and "client_secret."

## Requirements
- **Python 3:**
  - requests
  - python-dotenv
- **Spotify API Credentials:**
  - Client ID
  - Client Secret

## How to Get Spotify API Credentials
Follow this guide from Spotify Developers:
[How to get Spotify API Credentials](https://developer.spotify.com/documentation/web-api/concepts/apps)

## Contribution
Contributions are welcome! Please check the [contribution guidelines](CONTRIBUTING.md) before contributing.

## License
This project is licensed under the [MIT License](LICENSE).
