from spyne import Application, rpc, ServiceBase, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from spyne.model.primitive import Integer, String
from django.db import connection

class delete_service(ServiceBase):
    @rpc(Integer, _returns=Integer)
    def DeleteSong(ctx, id):
        try:
            cursor = connection.cursor()
            query = "DELETE FROM TBL_SONG WHERE ID_SONG=%s"
            cursor.execute(query, (id))
            connection.commit()
            return 1
        except Exception as e:
            print("Error delete data into database:", e)
            return 0
        finally:
            # Close database connection
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

delete_song_app = Application([delete_service],
                              tns='deleteservice',
                              in_protocol=Soap11(validator='lxml'),
                              out_protocol=Soap11())


delete_song = DjangoApplication(delete_song_app)