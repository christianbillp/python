import bokeh.plotting as bp
from bokeh.charts import show, output_file
from bokeh.models import Range1d
import pymysql.cursors
import pandas as pd


# Needs a connection to mySQL server:
connection = pymysql.connect(host='SERVERNAME',
                             user='USERNAME',
                             password='PASSWORD',
                             db='DATABASE',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


tl = {}
hl = {}
nodes = ['node0', 'node1', 'node2', 'node3']
graphwidth = 500
graphheight = 200
temperature_low = 15
temperature_high = 30
humidity_low = 20
humidity_high = 60
nvalues = 3000


def showall():
    for node in nodes:
        sql = 'SELECT * FROM {} ORDER BY id DESC LIMIT {}'.format(node,
                                                                  nvalues)
        df = pd.read_sql(sql, connection)
        ds = bp.ColumnDataSource(df)
        tl[node] = bp.figure(x_axis_type='datetime',
                               width=graphwidth,
                               height=graphheight,
                               title='{} - Temperature'.format(node))
        tl[node].y_range = Range1d(temperature_low, temperature_high)
        tl[node].line(source=ds, x='ts', y='temperature')
        hl[node] = bp.figure(x_axis_type='datetime',
                               width=graphwidth,
                               height=graphheight,
                               title='{} - Humidity'.format(node))
        hl[node].y_range = Range1d(humidity_low, humidity_high)
        hl[node].line(source=ds, x='ts', y='humidity', line_color="green")

    gpl = []
    for node in nodes:
        gpl.append([tl[node],hl[node]])
    output_file("layout.html")
    show(bp.gridplot(gpl))

showall()
connection.close()

