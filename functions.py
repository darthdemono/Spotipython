from urllib.parse import urlparse

def ms_to_min(ms):
    """
    Convert milliseconds to a formatted string representing minutes and seconds.

    Parameters:
    - ms (int): Duration in milliseconds.

    Returns:
    - str: Formatted string in the format "minutes:seconds".
    """
    seconds, millis = divmod(int(ms), 1000)
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes}:{seconds:02d}"

def key_value(key, value):
    """
    Format key-value pair as an uppercase string.

    Parameters:
    - key (str): Key.
    - value: (str): Value.

    Returns:
    - str: Formatted string in the format "KEY: VALUE".
    """
    return f"{key.upper()}: {value.upper()}"

def explicit_to_boolean():
    """
    Get user input for track explicitness and convert it to a boolean value.

    Returns:
    - bool: True if input is 'true', False otherwise.
    """
    explicit = input("Track Explicit: ")
    return explicit.lower() == "true"

def get_last_directory(url):
    """
    Extract the last segment of a URL path.

    Parameters:
    - url (str): URL.

    Returns:
    - str: The last segment of the URL path.
    """
    path = urlparse(url).path.rstrip('/')
    return path.split('/')[-1]

def print_separator_line():
    """
    Print a separator line for better output formatting.
    """
    print("_______________________________________________________________________")

def print_space_line():
    """
    Print an empty line for better output readability.
    """
    print("                                                                       ")
