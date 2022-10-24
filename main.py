from Playlist import Playlist
from Album import Album
from Artist import Artist
from Track import Track
from Pipeline import Pipeline
from TXTPersist import TXTPersist

from Settings import CLIENT_ID, CLIENT_SECRET

'''
TODO
1. hidden user and pw   OK
2. requirements    OK
3. alter execute for accept sequencial / thread
4. apply time tests and overhead thread (sequencial with threads \o/)
'''

persist = TXTPersist()

'''
playlist = Playlist(CLIENT_ID, CLIENT_SECRET, persist=persist, limit=2)
lt_playlists = playlist.extract(path_read='', path_write='data/playlists.txt')

album = Album(CLIENT_ID, CLIENT_SECRET, persist=persist)
album.extract(path_read='data/playlists.txt', path_write='data/albums.txt')

artist = Artist(CLIENT_ID, CLIENT_SECRET, persist=persist)
artist.extract(path_read='data/playlists.txt', path_write='data/artists.txt')

track = Track(CLIENT_ID, CLIENT_SECRET, persist=persist)
track.extract(path_read='data/playlists.txt', path_write='data/tracks.txt')
'''

PATHPLAYLIST = 'data/playlists.txt'
PATHALBUMS = 'data/albums.txt'
PATHARTISTS = 'data/artists.txt'
PATHTRACKS = 'data/tracks.txt'

playlist = Playlist(CLIENT_ID, CLIENT_SECRET, persist=persist, limit=2)
album = Album(CLIENT_ID, CLIENT_SECRET, persist=persist)
artist = Artist(CLIENT_ID, CLIENT_SECRET, persist=persist)
track = Track(CLIENT_ID, CLIENT_SECRET, persist=persist)

pipeline = Pipeline('t1')
pipeline.add_object(order=0, object=playlist, path_read=PATHPLAYLIST, path_write=PATHPLAYLIST)
pipeline.add_object(order=1, object=album, path_read=PATHPLAYLIST, path_write=PATHALBUMS)
pipeline.add_object(order=1, object=artist, path_read=PATHPLAYLIST, path_write=PATHARTISTS)
pipeline.add_object(order=1, object=track, path_read=PATHPLAYLIST, path_write=PATHTRACKS)

#pipeline.add_object(2, album)
pipeline.execute()


