from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import pymysql.cursors
import pandas as pd
import numpy as np

def getconf(filename):
	'''Creates dictionary from configuration file'''
	d = {}
	with open(filename, 'r') as file:
		for line in file:
			(key, val) = line.strip('\n').split(',')
			d[key] = val

	return d

XMLconfig = getconf("xmlserver.conf")
SQLconfig = getconf("sqlconf.conf")

connection = pymysql.connect(host=SQLconfig['host'],
                             user=SQLconfig['user'],
                             password=SQLconfig['password'],
                             db=SQLconfig['db'],
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
#connection = pymysql.connect(host='localhost',
#                             user='test',
#                             password='aabbccdd',
#                             db='test',
#                             charset='utf8mb4',
#                             cursorclass=pymysql.cursors.DictCursor)

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


# Create server
server = SimpleXMLRPCServer((XMLconfig['server_address'], int(XMLconfig["server_port"])), requestHandler=RequestHandler)
#server = SimpleXMLRPCServer(("deuscortex.com", 4343), requestHandler=RequestHandler)
server.register_introspection_functions()


# Function definitions - Consider moving to external library...
class XMLserver:
    '''XML-RPC server for mySQL interaction'''
    def __init__(self):
        pass

    def create_table(self, name, overwrite):
        ''' Create a new named table with values '''
        with connection.cursor() as c:
            if overwrite:
                c.execute('DROP TABLE IF EXISTS {}'.format(name))
                print('Table for {} dropped'.format(name))

            c.execute('CREATE TABLE {} (value1 real, value2 real, value3 real)'.format(name))
            print('Table for {} created'.format(name))

        return 0

    def add_data(self, table, value1, value2, value3):
        ''' Adds data into mySQL table '''
        with connection.cursor() as c:
            c.execute("insert into {} (value1, value2, value3) values ({},{},{})".format(table, value1, value2, value3))
            connection.commit()
        #print("Value {} added".format(value))

        return 0

    def generate_test_data(self, n):
        ''' Generates test data in mySQL table '''
        for i in range(n):
            self.add_data("test", np.random.rand(), np.random.rand(), np.random.rand())
        print("Test data generated!")
        return 0

def get_dataframe():
    ''' Returns dataframe as list to client '''
    df = pd.read_sql("select * from test", connection)
    return df.values.tolist()

# Register functions
server.register_instance(XMLserver())
server.register_function(lambda astr: '_' + astr, '_string')
server.register_function(get_dataframe, 'get_dataframe')

# Run the server's main loop
print("Server started")
server.serve_forever()





