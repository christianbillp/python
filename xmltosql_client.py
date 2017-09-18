import xmlrpc.client
import pandas as pd
import numpy as np

class XMLserver:
    ''' Client class for interacting with mySQL database '''

    def __init__(self, address):
        ''' Initializer '''
        self.address = address

    def create_table(self, overwrite):
        ''' Creates test table '''
        with xmlrpc.client.ServerProxy(self.address) as proxy:
            proxy.create_table("test", overwrite)
        return 0

    def add_data(self, value1, value2, value3):
        ''' Adds data '''
        with xmlrpc.client.ServerProxy(self.address) as proxy:
            proxy.add_data("test", value1, value2, value3)
        return 0

    def get_dataframe(self):
        ''' Returns pandas dataframe '''
        with xmlrpc.client.ServerProxy(self.address) as proxy:
            df = pd.DataFrame(proxy.get_dataframe())
        return df

    def generate_test_data(self, n):
        ''' Generate test data in server mySQL table '''
        with xmlrpc.client.ServerProxy(self.address) as proxy:
            proxy.generate_test_data(n)
        return 0

# Example code
interface = XMLserver("http://deuscortex.com:4343")
interface.create_table(1)
interface.generate_test_data(100)
interface.add_data(10, 10, 10)
df = interface.get_dataframe()
print(df)
df.plot()
