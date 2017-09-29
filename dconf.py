
def getconf(filename):
	d = {}
	with open(filename, 'r') as file:
		for line in file:
			(key, val) = line.strip('\n').split(',')
			d[key] = val

	return d

configuration = getconf("conf.conf")
print("Username from conf: {}".format(configuration["username"]))

print("Password from conf: {}".format(configuration["password"]))
