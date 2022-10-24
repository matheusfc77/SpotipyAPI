from ExtractionSpotipy import ExtractionSpotipy

class Album(ExtractionSpotipy):

    def __init__(self, client_id, client_secret, persist, verbose=True):
        ExtractionSpotipy.__init__(self, client_id, client_secret, verbose)
        self.persist = persist


    def request(self, playlist_id):
        if self.verbose: print("{}: START EXTRACTION ALBUMS".format(self.now()))

        urn = 'spotify:playlist:{}'.format(playlist_id)
        info_playlist = self.sp.playlist(urn, fields=None, market=None, additional_types=('track', ))

        lt_ids_albums = []
        for info in info_playlist['tracks']['items']:
          lt_ids_albums.append(info['track']['album']['id'])

        ls_albums = []
        for i, id_album in enumerate(list(set(lt_ids_albums))):
          urn_album = 'spotify:album:{}'.format(id_album)
          album = self.sp.album(urn_album)

          if self.verbose: 
            print("{}: {} spotify:album:{} {}".format(self.now(), i, id_album, album['name']))

          info_album = {
              'id': album['id'],
              'name': album['name'],
              'popularity': album['popularity']
          }
          ls_albums.append(info_album)

        if self.verbose: print("{}: END EXTRACTION ALBUMS".format(self.now()))
        return ls_albums


    def extract(self, path_read, path_write):
        lt_playlists = self.persist.read(path_read)
        lt_albumns_playlists = []
        
        for id, playlist_id in enumerate(lt_playlists):
            if self.verbose: print('{}: START ALBUMNS PLAYLIST {}'.format(self.now(), playlist_id))
            lt_albumns = self.request(playlist_id)
            lt_albumns_playlists.append(lt_albumns)
            if self.verbose: print('{}: END ALBUMNS PLAYLIST {}'.format(self.now(), playlist_id))

        lt_albumns_playlists = [item for sublist in lt_albumns_playlists for item in sublist]
        self.persist.write(path_write, lt_albumns_playlists)