import sqlite3
import random

conn = sqlite3.connect(":memory:")
c = conn.cursor()

class log:
    def __init__(self, name):
        self.name = name

    def table_create(self):
        c.execute(f'CREATE TABLE IF NOT EXISTS {self.name} (\
                  ID INTEGER PRIMARY KEY, \
                  time DATETIME DEFAULT CURRENT_TIMESTAMP, \
                  value REAL)')
        print(f"{self.name} created")

    def table_drop(self):
        c.execute(f'DROP TABLE IF EXISTS {self.name}')
        print(f"{self.name} deleted")

    def table_add_line(self, value):
        c.execute(f'INSERT INTO {self.name} (value) VALUES ({value})')

    def table_get_data(self):
        c.execute(f'SELECT * FROM {self.name}')
        result = c.fetchall()
        for row in result:
            print(row)

    # Write machine readable log
    def table_write_log(self):
        with open('newlog.txt', 'w') as file:
            c.execute(f'SELECT * FROM {self.name}')
            result = c.fetchall()
            for row in result:
                file.write(f"{str(row)}\n")

    # Write human readable log
    def table_write_report(self):
        with open('newlog.txt', 'w') as file:
            c.execute(f'SELECT * FROM {self.name}')
            result = c.fetchall()
            for row in result:
                file.write(f"[{str(row[0]):>3}] [{str(row[1])}]:\t{str(row[2]):>5}\n")

log1 = log('log1')
log1.table_create()
log1.table_create()
#log1.table_drop()

for _ in range(100):
    log1.table_add_line(random.randint(0,100))

log1.table_get_data()
log1.table_write_report()
