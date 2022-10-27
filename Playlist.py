from ExtractionSpotipy import ExtractionSpotipy

class Playlist(ExtractionSpotipy):

    def __init__(self, client_id, client_secret, persist, nm_playlists=50, verbose=True):
        ExtractionSpotipy.__init__(self, client_id, client_secret, verbose)
        self.nm_playlists = nm_playlists
        self.persist = persist
        self.MAX_LIMIT = 10


    def request(self, playlist_id='spotify'):
        if self.verbose: print("{}: START EXTRACTION PLAYLISTS".format(self.now()))

        playlists = self.sp.user_playlists(
            playlist_id, limit=self.nm_playlists if self.nm_playlists < self.MAX_LIMIT else self.MAX_LIMIT)
        lt_playlists = []

        while len(lt_playlists) < self.nm_playlists:
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


        if self.verbose: print("{}: END EXTRACTION PLAYLISTS".format(self.now()))
        return lt_playlists


    def extract(self, path_read, path_write):
        lt_playlists = self.request()
        self.persist.write(path_write, lt_playlists)