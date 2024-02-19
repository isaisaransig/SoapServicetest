from spyne import ComplexModel
from spyne.model.primitive import Integer, String

class Song(ComplexModel):
    ID_SONG = Integer
    SONG_NAME = String
    SONG_PATH = String
    PLAYS = Integer