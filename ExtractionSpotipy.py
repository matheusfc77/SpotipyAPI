import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from Now import Now


class ExtractionSpotipy(Now):

    def __init__(self, client_id, client_secret, verbose=True):
        client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
        self.verbose = verbose

    def request(self):
        raise NotImplementedError

    def extract(self, path_read, path_write):
        raise NotImplementedError
