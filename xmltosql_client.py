import xmlrpc.client

with xmlrpc.client.ServerProxy("http://deuscortex.com:4343") as proxy:

    print(proxy.create_table("test", 1))
    print(proxy.add_data("test", 100))
    print(proxy.add_data("test", 101))
    print(proxy.add_data("test", 102))
    print(proxy.add_data("test", 103))
    print(proxy.add_data("test", 104))
    print(proxy.add_data("test", 105))
