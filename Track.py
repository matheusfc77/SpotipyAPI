from ExtractionSpotipy import ExtractionSpotipy

class Track(ExtractionSpotipy):

    def __init__(self, client_id, client_secret, persist, verbose=True):
        ExtractionSpotipy.__init__(self, client_id, client_secret, verbose)
        self.persist = persist


    def request(self, playlist_id):
        '''
        Method for extraction tracks

        Args
            string (playlist_id): playlist for tracks extraction

        Return
            list: list with track data

        Raises
            TypeError: track_id is empty
        '''

        if self.verbose: print("{}: START EXTRACTION TRACKS".format(self.now()))

        urn = 'spotify:playlist:{}'.format(playlist_id)
        info_playlist = self.sp.playlist(urn, fields=None, market=None, additional_types=('track', ))

        lt_ids_tracks = []
        for info in info_playlist['tracks']['items']:
          try:
            lt_ids_tracks.append(info['track']['id'])
          except TypeError:
            print('PLAYLIST {}: TRACK WITH EMPTY FIELD'.format(playlist_id))

        ls_tracks = []
        for i, id_track in enumerate(list(set(lt_ids_tracks))):
          urn_track = 'spotify:track:{}'.format(id_track)
          track = self.sp.track(urn_track)

          if self.verbose: 
            print("{}: {} spotify:track:{} {}".format(self.now(), i, id_track, track['name']))

          info_track = {
              'id': track['id'],
              'name': track['name'],
              'popularity': track['popularity'],
              'duration_ms': track['duration_ms']
          }
          ls_tracks.append(info_track)

        if self.verbose: print("{}: END EXTRACTION TRACKS".format(self.now()))
        return ls_tracks


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
        lt_tracks_playlists = []
        for playlist_id in lt_playlists:
            if self.verbose: print('{}: START TRACKS PLAYLIST {}'.format(self.now(), playlist_id))
            lt_tracks = self.request(playlist_id)
            lt_tracks_playlists.append(lt_tracks)
            if self.verbose: print('{}: END TRACKS PLAYLIST {}'.format(self.now(), playlist_id))

        lt_tracks_playlists = [item for sublist in lt_tracks_playlists for item in sublist]
        self.persist.write(path_write, lt_tracks_playlists)