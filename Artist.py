from ExtractionSpotipy import ExtractionSpotipy

class Artist(ExtractionSpotipy):

    def __init__(self, client_id, client_secret, persist, verbose=True):
        ExtractionSpotipy.__init__(self, client_id, client_secret, verbose)
        self.persist = persist


    def request(self, playlist_id):
        if self.verbose: print("{}: START EXTRACTION ARTISTS".format(self.now()))

        urn = 'spotify:playlist:{}'.format(playlist_id)
        info_playlist = self.sp.playlist(urn, fields=None, market=None, additional_types=('track', ))

        lt_ids_artists = []
        for info in info_playlist['tracks']['items']:
          try:
            lt_ids_artists.append([art['id'] for art in info['track']['album']['artists']])
          except TypeError:
            print('PLAYLIST {}: ARTIST WITH EMPTY FIELD'.format(playlist_id))

        lt_ids_artists_flatten = [ele for sublist in lt_ids_artists for ele in sublist]
        ls_artists = []
        for i, id_artist in enumerate(list(set(lt_ids_artists_flatten))):
          urn_artist = 'spotify:artist:{}'.format(id_artist)
          artist = self.sp.artist(urn_artist)

          if self.verbose: 
            print("{}: {} spotify:artist:{} {}".format(self.now(), i, id_artist, artist['name']))

          info_artist = {
              'id': artist['id'],
              'name': artist['name'],
              'popularity': artist['popularity']
          }
          ls_artists.append(info_artist)

        if self.verbose: print("{}: END EXTRACTION ARTISTS".format(self.now()))
        return ls_artists


    def extract(self, path_read, path_write):
        lt_playlists = self.persist.read(path_read)
        lt_artists_playlists = []
        for playlist_id in lt_playlists:
            if self.verbose: print('{}: START ARTISTS PLAYLIST {}'.format(self.now(), playlist_id))
            lt_artists = self.request(playlist_id)
            lt_artists_playlists.append(lt_artists)
            if self.verbose: print('{}: END ARTISTS PLAYLIST {}'.format(self.now(), playlist_id))

        lt_artists_playlists = [item for sublist in lt_artists_playlists for item in sublist]
        self.persist.write(path_write, lt_artists_playlists)

      
