<div align="center">
  <img src="https://miro.medium.com/v2/resize:fit:1200/0*eIfW4F5Q4ZQs6X99" width="500" align="center">
  <h1>Spotipython</h1>
  
  <p align="center">
      <i>An open-source project for fetching Spotify track and album data programmatically using Python and the Spotify API.</i>
  </p>
  
  [![GitHub Issues](https://img.shields.io/github/issues/darthdemono/Spotipython?style=for-the-badge)](https://github.com/darthdemono/Spotipython/issues)
  [![GitHub Forks](https://img.shields.io/github/forks/darthdemono/Spotipython?style=for-the-badge)](https://github.com/darthdemono/Spotipython/network)
  [![GitHub Stars](https://img.shields.io/github/stars/darthdemono/Spotipython?style=for-the-badge)](https://github.com/darthdemono/Spotipython/stargazers)
  [![License](https://img.shields.io/github/license/darthdemono/Spotipython?style=for-the-badge)](LICENSE)
  [![Last Commit](https://img.shields.io/github/last-commit/darthdemono/Spotipython?style=for-the-badge)](https://github.com/darthdemono/Spotipython/commits/main)
  [![Python Version](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge)](https://www.python.org/downloads/)

</div>


## Introduction
Spotipython is a Python project that utilizes the Spotify API to fetch detailed information about albums, artists, and tracks. Whether you have an album link or want to search for specific tracks, Spotipython provides scripts to gather the data you need programmatically.

## Project Structure
The project is organized with the following directory structure:

- **Spotipython/**
  - **spotify_album.py:** Script to fetch information about a Spotify album and its tracks.
  - **spotify_search.py:** Script to search for tracks on Spotify based on user input.
  - **spotify_client.py:** Module defining the `SpotifyAPI` class for handling authentication and making requests to the Spotify API.
  - **.env:** Configuration file containing your Spotify API credentials (client_id and client_secret).
  - **functions.py:** Module with utility functions used across different scripts.
  - **requirements.txt:** File listing the Python dependencies required for the project.


## Scripts
### spotify_album.py
- Fetches information about a Spotify album and its tracks.
- Displays detailed information about the album, such as total tracks, album type, artist followers, genres, and additional details for each track.
- **Inputs:** Album Link
#### How to Use:
```cmd
python spotify_album.py
```
Follow the prompts and provide the Spotify Album URL when requested.
### spotify_search.py
- Searches for tracks on Spotify based on user input (album, artist, explicit).
- Retrieves information about the tracks, filters them based on explicit content, and prints detailed information about each track, including album details and external links.
- **Inputs:** Album Name, Artist Name, Explicit (True or, False)
#### How to Use:
```cmd
python spotify_search.py
```
Follow the prompts and provide the necessary information when requested.

### spotify_client.py
- Defines a SpotifyAPI class that handles authentication and makes requests to the Spotify API.
- Provides methods to obtain an access token, fetch resources (like albums, artists, tracks), and perform searches.
#### How to Use:
```python
# Import the SpotifyAPI class in your own script
from spotify_client import SpotifyAPI

# Create an instance of the SpotifyAPI class
spotify = SpotifyAPI("your_client_id", "your_client_secret")

# Now you can use the SpotifyAPI instance to interact with the Spotify API
```

### functions.py
- Contains utility functions used in other files.
- Functions include converting milliseconds to minutes, formatting key-value pairs, converting explicit input to a boolean, extracting the last directory from a URL, and printing separator and space lines.

### Dotenv
- Dotenv file contains your "client_id" and "client_secret."

## Requirements
- **Python 3:**
```python
  requests>=2.26.0
  python-dotenv>=0.19.2
```
- **Spotify API Credentials:**
  - Client ID
  - Client Secret

## How to Get Spotify API Credentials
Follow this guide from Spotify Developers:
[How to get Spotify API Credentials](https://developer.spotify.com/documentation/web-api/concepts/apps)

## Installation: 
1. Clone the repository:
   ```cmd
   git clone https://github.com/darthdemono/Spotipython.git
   cd Spotipython
   ```
2. Install the required packages:
   ```cmd
   pip install -r requirements.txt
   ```
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Contribution
Contributions are welcome! Please check the [Contribution Guidelines](CONTRIBUTING.md) before contributing.

## Code of Conduct
Please review our [Code of Conduct](CODE_OF_CONDUCT.md) before participating in the project.
