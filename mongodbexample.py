# %%
from pymongo import MongoClient
import pandas as pd


client = MongoClient('localhost', 27017)

db = client['test-db']

collection = db['test-collection']

import datetime
post = {"author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}


posts = db.posts
post_id = posts.insert_one(post).inserted_id
post_id

#%%
import pprint
pprint.pprint(posts.find_one())
#%%
data = {'name' : 'nodex',
        'temp' : 28,
        'humi' : 31,}

collection.insert_one(data)
#%%


for item in collection.find({'name':'nodex'}):
    pprint.pprint(item)

#%%
df = pd.DataFrame.from_records(collection.find({'name':'nodex'}))
#%%
from pymongo import MongoClient

client = MongoClient("mongodb://nodes:aabbccdd@192.168.0.100/nodes") # defaults to port 27017
db = client.nodes

print(db.)


#%%
from pymongo import MongoClient

def send_data(data):
    db = MongoClient('deuscortex.com', 27017)['test-db']
#    db = client['test-db']
    collection = db['test-collection']
    collection.insert_one(data)
    
data = {'name' : 'nodex',
        'temp' : 28,
        'humi' : 31,}

send_data(data)

#%%
df = pd.DataFrame.from_records(collection.find({'name':'nodex'}))
df
#%%
from pymongo import MongoClient
import pandas as pd


def get_df():
    df = pd.DataFrame([])

    with MongoClient('mongodb://twitter:aabbccdd@deuscortex.com:27017/nlp') as client:
        data = [entry for entry in client['nlp']['twitter'].find()]
        
    for value in ['lang', 'text', 'created_at']:
        df[value] = [entry[value] for entry in data]
    
    df['user_id'] = [entry['user']['id'] for entry in data]
    df['screen_name'] = [entry['user']['screen_name'] for entry in data]
    df['hashtags'] = [[hashtag['text'] for hashtag in item] for item in [entry['entities']['hashtags'] for entry in data]];

    return df, data


df, data = get_df()
#%%

with MongoClient('mongodb://twitter:aabbccdd@deuscortex.com:27017/nlp') as client:
    data = client['nlp']['twitter'].count()

print(data)

#[tag for tag in [entry['entities']['hashtags'] for entry in data]]


#data[0].keys()











