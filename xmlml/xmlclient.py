import xmlrpc.client
import numpy as np
from scipy.linalg import svd


array = np.array([[1.12, 2.34, 3.45, 4.56],
				  [5.12, 6.34, 7.45, 8.56],
				  [9.12, 7.34, 5.45, 3.56],
				  [8.12, 6.34, 4.45, 2.56]])
remote_result = 0
local_result = 0

def get_conf(filename):
	with open(filename, "r") as file:
		line = file.readline()
		
		return line

server = get_conf('client.conf')

def matmultest():
	with xmlrpc.client.ServerProxy(server) as proxy:
		remote_result = np.array(proxy.mmul(array.tolist()))

	print("Local result: {}".format(np.matmul(array, array)))
	print("Remote result: {}".format(remote_result))

def svdtest():
	with xmlrpc.client.ServerProxy(server) as proxy:
		remote_result = proxy.svd(array.tolist())
	
	local_result = svd(array, full_matrices=False)
	remote_result = (np.array(remote_result[0]),np.array(remote_result[1]),np.array(remote_result[2]))
	
		
	print("local")
	for sub in local_result:
		for value in sub:
			print(value.round(3))
	
	print("remote")
	for sub in remote_result:
		for value in sub:
			print(value.round(3))

svdtest()
