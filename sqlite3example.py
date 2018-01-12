# %% sqlite3 mere generelle funktioner
import sqlite3

class DBthing:

    def __init__(self, filename, debug=0):
        self.filename = filename
        self.c = sqlite3.connect(filename).cursor()
        self.debug = debug

    def create_table(self, name, n_columns):
        """Creates a table with [name] containing auto-named [n_columns]"""
        columns = ' TEXT, '.join(['col' + str(i) for i in range(n_columns)])
        sql_command = f'CREATE TABLE IF NOT EXISTS {name} ({columns})'
        print(sql_command) if self.debug == 1 else 0
        self.c.execute(sql_command)

    def create_table_named(self, name, column_names):
        """Creates a table with [name] containing auto-named [n_columns]"""
        columns = ' TEXT, '.join(column_names)
        sql_command = f'CREATE TABLE IF NOT EXISTS {name} ({columns})'
        print(sql_command) if self.debug == 1 else 0
        self.c.execute(sql_command)

    def add_data(self, table_name, values):
        """Adds data into [table_name], [values] are represented as a list"""
        val = ','.join([''+str(value) for value in values])
        sql_command = f'INSERT INTO {table_name} VALUES ({val})'
        print(sql_command) if self.debug == 1 else 0
        self.c.execute(sql_command)

    def show_data(self, table_name):
        """Prints out all data from [table_name]"""
        sql_command = f'SELECT * FROM {table_name}'
        print(sql_command) if self.debug == 1 else 0
        [print(row) for row in self.c.execute(sql_command)]


if __name__ == '__main__':
    import random

    # Specify desired databases and tables
    n_db = 2
    tables = {'ulla' : 5, 'bjarne' : 10}

    databases = [DBthing(':memory:') for _ in range(n_db)]

    for db in databases:

        for item in tables:

            db.create_table(item, tables[item])

            for _ in range(5):
                db.add_data(item, [random.randint(10, 99) for _ in range(tables[item])])

            print(f'Showing data for table: {item} in database: {db}')
            db.show_data(item)