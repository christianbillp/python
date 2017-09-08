import sqlite3
import datetime
import paho.mqtt.client as mqtt

conn = sqlite3.connect(':memory')
c = conn.cursor()


class node:
    def __init__(self, name, address):
        self.name = name
        self.address = address

    def create_table(self, overwrite):
        if overwrite:
            c.execute('DROP TABLE IF EXISTS {}'.format(self.name))
            print('Table for {} dropped'.format(self.name))
            c.execute('CREATE TABLE {} (time timestamp, temperature REAL, humidity REAL, output REAL)'.format(self.name))
            print('Table for {} created'.format(self.name))
        else:
            c.execute('CREATE TABLE {} (time timestamp, temperature REAL, humidity REAL, output REAL)'.format(self.name))
            print('Table for {} created'.format(self.name))

    def add_data(self, temperature, humidity, outputvalue):
        c.execute("INSERT INTO {} VALUES (?,?,?,?)".format(self.name), (datetime.datetime.now(),
                                                                        temperature,
                                                                        humidity,
                                                                        outputvalue))
        conn.commit()

    def show_data(self, mode):
        if mode == "display":
            for row in c.execute('SELECT * FROM {}'.format(self.name)):
                print(row)
        elif mode == "count":
            print("Entries for node" + str(node) + " : ", end="")
            counter = 0
            for row in c.execute('SELECT * FROM {}'.format(self.name)):
                counter += 1
            print(counter)

    def cleanup(self):
        c.execute('DELETE FROM {} WHERE temperature="0.0"'.format(self.name))
        c.execute('DELETE FROM {} WHERE humidity="0.0"'.format(self.name))
        conn.commit()

    def get_values_from_database(self, scale):
        self.scale = scale
        datestamp = []
        temperature = []
        humidity = []
        outputs = []
        for row in c.execute('SELECT * FROM {} ORDER BY time'.format(self.name)):
            datestamp.append(row[0])
            temperature.append(row[1])
            humidity.append(row[2])
            outputs.append(row[3])
        inputvalues = datestamp, temperature, humidity, outputs
        outputvalues = []
        running = []
        counter = 0
        for list in inputvalues:
            outputvalues.append([])
            if type(list[0]) == datetime.datetime:
                for value in list:
                    running.append(1)
                    if len(running) == scale:
                        outputvalues[counter].append(value)
                        running = []
            else:
                for value in list:
                    running.append(value)
                    if len(running) == scale:
                        outputvalues[counter].append(sum(running)/len(running))
                        running = []
            counter += 1
        return outputvalues

try:
    # node1.show_data("display")
    # node1.add_data(34.5, 29.1, 1)
finally:
    conn.close()