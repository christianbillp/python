# %% https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/
import tweepy
import nltk
from tweepy import OAuthHandler

consumer_key = 'nSSRWzKyvBS8D2AnGxOyw'
consumer_secret = 'Yi3ghba1JW5RkYfLQ861Phx8IAvOloHMFdMQCFfPA'
access_token = '314960277-exdESOVudxMr1lGwW0GHgLcaT2WJmniRZQjJGsU7'
access_secret = 'H0Q83J5TsKbknLkiypAF9d2reZjMd8ntq1byUvtPFS3hv'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

# %% See recent
n = 10
for status in tweepy.Cursor(api.home_timeline).items(n):
    print(status.text)

# %% Search for tag
n = 2300    #Seems to be the limit
tag = 'trustpilot'
rl = []
for status in tweepy.Cursor(api.search, q=tag).items(n):
    rl.append(status.text)
# %% Tweet filtering
import re
from nltk.corpus import stopwords

def clean_tokenize(input_tweet):
    '''Removes tags and hyperlinks from tweet'''
    rs = " ".join(filter(lambda x:x[0]!='#', input_tweet.split()))
    rs = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', rs, flags=re.MULTILINE)

    rt = nltk.word_tokenize(rs)

    return rt

def token_compare(rl):
    for entry in rl:
        print('Cleaned: {}\n'.format(clean_tokenize(entry)))
#        print('Original: {}\n'.format(entry))

# %%
ts = ' '.join(rl)
text = nltk.Text(clean_tokenize(ts))
text.concordance('trust')
