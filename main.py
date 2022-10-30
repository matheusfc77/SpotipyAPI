from Playlist import Playlist
from Album import Album
from Artist import Artist
from Track import Track
from Pipeline import Pipeline
from TXTPersist import TXTPersist

from Settings import CLIENT_ID, CLIENT_SECRET
from Time import calculate_time


persist = TXTPersist()

PATHPLAYLIST = 'data/playlists.txt'
PATHALBUMS = 'data/albums.txt'
PATHARTISTS = 'data/artists.txt'
PATHTRACKS = 'data/tracks.txt'
NM_PLAYLISTS = 2

playlist = Playlist(CLIENT_ID, CLIENT_SECRET, persist=persist, nm_playlists=NM_PLAYLISTS)
album = Album(CLIENT_ID, CLIENT_SECRET, persist=persist)
artist = Artist(CLIENT_ID, CLIENT_SECRET, persist=persist)
track = Track(CLIENT_ID, CLIENT_SECRET, persist=persist)

pipeline = Pipeline()
pipeline.add_object(order=0, object=playlist, path_read=PATHPLAYLIST, path_write=PATHPLAYLIST)
pipeline.add_object(order=1, object=album, path_read=PATHPLAYLIST, path_write=PATHALBUMS)
pipeline.add_object(order=1, object=artist, path_read=PATHPLAYLIST, path_write=PATHARTISTS)
pipeline.add_object(order=1, object=track, path_read=PATHPLAYLIST, path_write=PATHTRACKS)

@calculate_time
def execute_pipeline(pipeline):
    pipeline.execute(parallel=True)

LEN_TEST = 3
lt_time = []
for _ in range(LEN_TEST):
    lt_time.append(execute_pipeline(pipeline))

print(lt_time)


