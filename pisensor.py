#%%
from sqlite3example import DBthing
import random

db = DBthing('node0.sqlite', 1)

def get_sensor_values():
    return [random.randint(0,30), random.randint(0,30)]


if __name__ == '__main__':
    # Only on first run
#    db.create_table('node0', 2)

    # Add some data
    db.add_data('node0', get_sensor_values())
    db.add_data('node0', get_sensor_values())
    db.add_data('node0', get_sensor_values())

    # Show data currently in database
    db.show_data('node0')