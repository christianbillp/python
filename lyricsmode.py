import pylast
import PyLyrics
import time
import nltk
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Information from Last.fm
API_KEY = "YOUR KEY HERE"
API_SECRET = "YOUR SECRET HERE"
username = "YOUR USERNAME HERE"
password_hash = "YOUR HASH HERE"
network = pylast.LastFMNetwork(api_key=API_KEY,
                               api_secret=API_SECRET,
                               username=username,
                               password_hash=password_hash)


lastfm_user = network.get_user(username)


def song_info():
    current = lastfm_user.get_now_playing()
    song_artist = current.artist.get_name()
    song_title = current.get_title()

    if ' - ' in song_title:
        song_title = song_title.split('-')
        return song_artist, song_title[0]
    else:
        return song_artist, song_title


def generate_output(page_title, song_lyrics):
    f = open('/var/www/html/lyrics/index.html', 'w')
    c = song_lyrics.split('\n')
    lyrics_part1 = '<br>'.join(c[0:len(c)//2])
    lyrics_part2 = '<br>'.join(c[len(c)//2+1:len(c)])


    message = """<html>
    <head></head>
    <meta http-equiv="refresh" content="5; URL=http://lyrics.0ohm.dk">
    <font face="verdana">
    <body><h1 align="center">{0}</h1>
        <p>
        <table align="center" cellpadding="10">
            <tr>
                <td valign="top">{1}</td>
                <td valign="top">{2}</td>
            </tr>
        </table>
        </p>
    </font>
    <center>    
        <img src="ldp.png" />
    </center>
    </body>
    <br>
    </html>""".format(page_title, lyrics_part1, lyrics_part2)
    f.write(message)
    f.close()

def create_lpd(song_title, song_lyrics):
    tokens = nltk.word_tokenize(song_lyrics.lower())
    text = nltk.Text(tokens)
    fig = plt.figure(figsize=(8,4))
    text.dispersion_plot(song_title.lower().split(' '))
    fig.savefig('ldp.png')

while True:
    try:
        song_artist, song_title = song_info()
        print("Looking up: {} - {}".format(song_artist, song_title))
        song_lyrics = PyLyrics.PyLyrics.getLyrics(song_artist, song_title)
        generate_output("{} - {}".format(song_artist, song_title), song_lyrics)
        create_lpd(song_title, song_lyrics)
        print("Process Successful")

    except ValueError:
        print("Not found")
        pass
    except AttributeError:
        print("No connection")
        pass
    except pylast.WSError:
        print("Rejected by pylast")
        pass
    time.sleep(10)

