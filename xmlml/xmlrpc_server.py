from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import numpy as np
from scipy.linalg import svd

# Read configuration file
def get_conf(filename):
    with open(filename, "r") as file:
        line = file.readline().split(',')
        return line

server, port = get_conf('server.conf')


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


# Create server
server = SimpleXMLRPCServer((server, int(port)),
                            requestHandler=RequestHandler)
server.register_introspection_functions()


# Just for testing
def adder_function(x,y):
    return x + y
server.register_function(adder_function, 'add')


# Matrix multiplication
def mmul(array):
    print("Matrix multiplication called")
    work = np.array(array)
    result = np.matmul(array, array)

    return result.tolist()
server.register_function(mmul, 'mmul')


# Singular Value Decomposition
def dcsvd(array):
    print("SVD called")
    matrix = np.array(array)
    U,S,V = svd(matrix,full_matrices=False)
    result = [U.tolist(), S.tolist(), V.tolist()]

    return result
server.register_function(dcsvd, 'svd')


# Run the server's main loop
print("Server started")
server.serve_forever()

