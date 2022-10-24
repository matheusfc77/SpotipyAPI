from ExtractionSpotipy import ExtractionSpotipy

class Playlist(ExtractionSpotipy):

    def __init__(self, client_id, client_secret, persist, limit=50, verbose=True):
        ExtractionSpotipy.__init__(self, client_id, client_secret, verbose)
        self.limit = limit
        self.persist = persist


    def request(self, playlist_id='spotify'):
        if self.verbose: print("{}: START EXTRACTION PLAYLISTS".format(self.now()))

        playlists = self.sp.user_playlists(playlist_id, limit=self.limit if self.limit < 30 else 30)
        lt_playlists = []

        while len(lt_playlists) < self.limit:
            for i, playlist in enumerate(playlists['items']):
                if self.verbose: 
                    print("{}: {} {} {}".format(self.now(), i, playlist['uri'], playlist['name']))
                
                info_playlist = {
                    'id': playlist['id'],
                    'description': playlist['description'],
                    'name': playlist['name'],
                    'external_urls': playlist['external_urls']['spotify']
                }
                lt_playlists.append(info_playlist)
            
            if playlists['next']:
                playlists = self.sp.next(playlists)
            #else: playlists = None
            #playlists = None

        if self.verbose: print("{}: END EXTRACTION PLAYLISTS".format(self.now()))
        return lt_playlists


    def extract(self, path_read, path_write):
        lt_playlists = self.request()
        self.persist.write(path_write, lt_playlists)