from ExtractionSpotipy import ExtractionSpotipy

class Track(ExtractionSpotipy):

    def __init__(self, client_id, client_secret, persist, verbose=True):
        ExtractionSpotipy.__init__(self, client_id, client_secret, verbose)
        self.persist = persist


    def request(self, playlist_id):
        if self.verbose: print("{}: START EXTRACTION TRACKS".format(self.now()))

        urn = 'spotify:playlist:{}'.format(playlist_id)
        info_playlist = self.sp.playlist(urn, fields=None, market=None, additional_types=('track', ))

        lt_ids_tracks = []
        for info in info_playlist['tracks']['items']:
          lt_ids_tracks.append(info['track']['id'])

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
        lt_playlists = self.persist.read(path_read)
        lt_tracks_playlists = []
        for id, playlist_id in enumerate(lt_playlists):
            if self.verbose: print('{}: START TRACKS PLAYLIST {}'.format(self.now(), playlist_id))
            lt_tracks = self.request(playlist_id)
            lt_tracks_playlists.append(lt_tracks)
            if self.verbose: print('{}: END TRACKS PLAYLIST {}'.format(self.now(), playlist_id))

        lt_tracks_playlists = [item for sublist in lt_tracks_playlists for item in sublist]
        self.persist.write(path_write, lt_tracks_playlists)