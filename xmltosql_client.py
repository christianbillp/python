import xmlrpc.client
import pandas as pd


with xmlrpc.client.ServerProxy("http://deuscortex.com:4343") as proxy:
#    print(proxy.create_table("test", 1))
#    print(proxy.add_data("test", 100))
    k = proxy.get_dataframe()
    print(k)
    df = pd.DataFrame(k)

print(df)
