from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import pymysql.cursors
import pandas as pd

connection = pymysql.connect(host='localhost',
                             user='test',
                             password='aabbccdd',
                             db='test',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


# Create server
server = SimpleXMLRPCServer(("deuscortex.com", 4343), requestHandler=RequestHandler)
server.register_introspection_functions()


# Function definitions - Consider moving to external library...
class XMLserver:
    def __init__(self):
        pass

    def create_table(self, name, overwrite):
        ''' Create a new named table with values '''
        with connection.cursor() as c:
            if overwrite:
                c.execute('DROP TABLE IF EXISTS {}'.format(name))
                print('Table for {} dropped'.format(name))

            c.execute('CREATE TABLE {} (value real)'.format(name))
            print('Table for {} created'.format(name))

        return 0

    def add_data(self, table, value):
        with connection.cursor() as c:
            c.execute("INSERT INTO {} (value) VALUES ({})"
                      .format(table, value))

            connection.commit()
        #print("Value {} added".format(value))

        return 0

def get_dataframe():
    df = pd.read_sql("select * from test", connection)
    return df.values.tolist()

# Register functions
server.register_instance(XMLserver())
server.register_function(lambda astr: '_' + astr, '_string')
server.register_function(get_dataframe, 'get_dataframe')

# Run the server's main loop
#print("Server started")
server.serve_forever()


#df = pd.read_sql("select * from test", connection)
#print(df)
#s = XMLserver()
#print(88)
#s.add_data("test", 44)

#k = get_dataframe()
#print(k)






