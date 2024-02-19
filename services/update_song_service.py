from spyne import Application, rpc, ServiceBase, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from spyne.model.primitive import Integer, String
from django.db import connection

class update_service(ServiceBase):
    @rpc(Integer, String, String, Integer, _returns=Integer)
    def UpdateSong(ctx, id, song_name, song_path, plays):
        try:
            cursor = connection.cursor()
            query = "UPDATE TBL_SONG SET SONG_NAME=%s, SONG_PATH=%s, PLAYS= %s WHERE ID_SONG=%s"
            cursor.execute(query, (song_name, song_path, plays, id))
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

update_song_app = Application([update_service],
                              tns='updateservice',
                              in_protocol=Soap11(validator='lxml'),
                              out_protocol=Soap11())


update_song = DjangoApplication(update_song_app)