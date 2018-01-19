# %% Rejseplanen
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

stations = {'Nørrebro St.' : '000001989', 
            'Griffenfeldsgade (Rantzausgade)' : '000003078',
            'H.C. Ørsteds Vej (Gammel Kongevej)' : '000001424',
            'Københavns Hovedbanegård' : '008600626',
            'Nørrebrogade' : '000001576',}

base_url = 'http://xmlopen.rejseplanen.dk/bin/rest.exe'

def find_station(search):
    request = f'{base_url}/location?input="{search}"'
    with urllib.request.urlopen(request) as f:
        root = ET.parse(f).getroot()
        [print(child.items()) for child in root];
        
def departureboard(stationid):
    request = f'{base_url}/departureBoard?id={stationid}'
    print(request)
    with urllib.request.urlopen(request) as f:
        root = ET.parse(f).getroot()
        [print(child.items()[0], child.items()[3], child.items()[6]) for child in root];

def trip(originid, destid):
    now = (datetime.now() + timedelta(minutes=1)).strftime('%H:%M')
    request = f'{base_url}/trip?originId={originid}&destId={destid}&time={now}'
    with urllib.request.urlopen(request) as f:
        root = ET.parse(f).getroot()
        for trip in root:
            for leg in trip:
                if leg.items()[1][1] != 'WALK':
                    time = leg[0].items()[3][1]
                    timeob = datetime.strptime(time, '%H:%M')
                    timedifference = timeob - datetime.now()
                    print(leg.items()[0][1], '-' ,leg[0].items()[3][1], '-',
                          ':'.join(str(timedifference).split(' ')[2].split(':')[0:2]))

if __name__ == '__main__':
    pass                   
    # %% Seach for station names
    find_station('norrebro')
    
    # %% Show departureboard information for stop
    departureboard(stations['Nørrebro St.'])
    
    # %% Show trip information between dictionaried stations
    trip(stations['Griffenfeldsgade (Rantzausgade)'], stations['Nørrebro St.'])