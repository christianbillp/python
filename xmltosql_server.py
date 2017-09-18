from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import pymysql.cursors

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
def create_table(name, overwrite):
    ''' Create a new named table with values '''
    with connection.cursor() as c:
        if overwrite:
            c.execute('DROP TABLE IF EXISTS {}'.format(name))
            print('Table for {} dropped'.format(name))
            c.execute('CREATE TABLE {} (value)'.format(name))
            print('Table for {} created'.format(name))
        else:
            c.execute('CREATE TABLE {} (value)'.format(name))
            print('Table for {} created'.format(name))

    return 0


def add_data(table, value):
    with connection.cursor() as c:
        c.execute("INSERT INTO {} (value) VALUES ({})"
                  .format(table, value))

        connection.commit()
        #print("Value {} added".format(value))

    return 0

# Register functions
server.register_function(add_data, 'add_data')
server.register_function(create_table, 'create_table')

print("Server started")

# Run the server's main loop
server.serve_forever()











