from spyne import Application, rpc, ServiceBase, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from spyne.model.primitive import Integer, String
from django.db import connection

class create_service(ServiceBase):
    @rpc(String, String, Integer, _returns=Integer)
    def CreateSong(ctx, song_name, song_path, plays):
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO TBL_SONG (SONG_NAME, SONG_PATH, PLAYS) VALUES (%s, %s, %s)", (song_name, song_path, plays))
            connection.commit()
            return 1
        except Exception as e:
            print("Error inserting data into database:", e)
            return 0
        finally:
            # Close database connection
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

create_song_app = Application([create_service],
                              tns='createservice',
                              in_protocol=Soap11(validator='lxml'),
                              out_protocol=Soap11())

# Create the Django application for the SOAP service to create a song
create_song = DjangoApplication(create_song_app)