from ExtractionSpotipy import ExtractionSpotipy

class Album(ExtractionSpotipy):

    def __init__(self, client_id, client_secret, persist, verbose=True):
        ExtractionSpotipy.__init__(self, client_id, client_secret, verbose)
        self.persist = persist


    def request(self, playlist_id):
        '''
        Method for extraction albumns

        Args
            string (playlist_id): playlist for albumns extraction

        Return
            list: list with album data

        Raises
            TypeError: album_id is empty
        '''

        if self.verbose: print("{}: START EXTRACTION ALBUMS".format(self.now()))

        urn = 'spotify:playlist:{}'.format(playlist_id)
        info_playlist = self.sp.playlist(urn, fields=None, market=None, additional_types=('track', ))

        lt_ids_albums = []
        for info in info_playlist['tracks']['items']:
          try:
            lt_ids_albums.append(info['track']['album']['id'])
          except TypeError:
            print('PLAYLIST {}: ALBUM WITH EMPTY FIELD'.format(playlist_id))

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
        '''
        Method for read and write data

        Args
            string (path_read): data source
            string (path_write): path for save the data

        Return 
            None
        '''

        lt_playlists = self.persist.read(path_read)
        lt_albumns_playlists = []
        
        for playlist_id in lt_playlists:
            if self.verbose: print('{}: START ALBUMNS PLAYLIST {}'.format(self.now(), playlist_id))
            lt_albumns = self.request(playlist_id)
            lt_albumns_playlists.append(lt_albumns)
            if self.verbose: print('{}: END ALBUMNS PLAYLIST {}'.format(self.now(), playlist_id))

        lt_albumns_playlists = [item for sublist in lt_albumns_playlists for item in sublist]
        self.persist.write(path_write, lt_albumns_playlists)