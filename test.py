def get_conf(filename):
    with open(filename, "r") as file:
        line = file.readline().split(',')
    return line

server, port = get_conf('configuration.conf')
