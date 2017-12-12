#%% DST.dk - Basic Functions
import requests
import pandas as pd
import pprint

'''
                                description  id
0                        Befolkning og valg  02
1                                Levevilkår  05
2                       Uddannelse og viden  03
3                           Kultur og kirke  18
4               Arbejde, indkomst og formue  04
5                         Priser og forbrug  06
6   Nationalregnskab og offentlige finanser  14
7                    Penge og kapitalmarked  16
8                           Udenrigsøkonomi  13
9                    Erhvervslivet på tværs  07
10                  Erhvervslivets sektorer  11
11                Geografi, miljø og energi  01
12                               Tværgående  19
''';

def explore_subject(idn):
    '''Explore subjects to find subject ids'''
    url = f'http://api.statbank.dk/v1/subjects/{str(idn)}?format=JSON'
    r = requests.get(url=url)
    pprint.pprint(r.json())

def explore_table(idn):
    '''Explore tables to find table ids for data extraction'''
    url = f'http://api.statbank.dk/v1/tables?subjects={str(idn)}'
    r = requests.get(url=url)
    pprint.pprint(r.json())

def get_data(url):
    '''Construct URL with: http://api.statbank.dk/console#data'''
    r = requests.get(url=url)
    work = r.text.strip('\ufeff').split('\r\n')
    work = [line.split(';') for line in work]
    df = pd.DataFrame(work[1:], columns=work[0])

    return df

#%%
df = get_data("http://api.statbank.dk/v1/data/FOLK1B/CSV?K%C3%98N=TOT&ALDER=IALT&OMR%C3%85DE=000&Tid=*")
df.head(10)

#%%
#df = get_data('http://api.statbank.dk/v1/data/FOLK1B/CSV?OMR%C3%85DE=*&K%C3%98N=*&ALDER=*&Tid=*&STATSB=0000')
df.head()