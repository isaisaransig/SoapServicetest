from spyne import Application, rpc, ServiceBase, Array
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from django.db import connection
from spyne import ComplexModel
from spyne.model.primitive import Integer, String

class Song(ComplexModel):   
    ID_SONG = Integer
    SONG_NAME = String
    SONG_PATH = String
    PLAYS = Integer

class read_service(ServiceBase):
    @rpc(_returns=Array(Song))
    def GetAllSongs(ctx):
        songs = []
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM TBL_SONG")
            rows = cursor.fetchall()
            for row in rows:
                song = Song(ID_SONG=row[0], SONG_NAME=row[1], SONG_PATH=row[2], PLAYS=row[3])
                songs.append(song)
        except Exception as e:
            print("Error retrieving data from database:", e)
            songs = []  # Empty list in case of error
        finally:
            cursor.close()
        return songs

read_song_app = Application([read_service], 'readservice',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())
read_song = DjangoApplication(read_song_app)
