from urllib.parse import urlparse
def ms_to_min(ms):
    seconds, millis = divmod(int(ms), 1000)
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes}:{seconds:02d}"

def key_value(key, value):
    return f"{key.upper()}: {value.upper()}"

def explicit_to_boolean():
    explicit = input("Track Explicit: ")
    return explicit.lower() == "true"

def get_last_directory(url):
    path = urlparse(url).path.rstrip('/')
    return path.split('/')[-1]

def print_separator_line():
    print("_______________________________________________________________________")

def print_space_line():
    print("                                                                       ")