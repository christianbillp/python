import pylast
import PyLyrics
import time

#==================================================
# Requires a last.fm username connected to Spotify.
#==================================================


API_KEY = "API_KEY"
API_SECRET = "API_SECRET"
username = "USERNAME"
password_hash = 'PASSWORD_HASH'
network = pylast.LastFMNetwork(api_key=API_KEY,
                               api_secret=API_SECRET,
                               username=username,
                               password_hash=password_hash)

lastfm_user = network.get_user('LASTFM_USERNAME')

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
    f = open('index.html', 'w')
    c = song_lyrics.split('\n')
    lyrics_part1 = '<br>'.join(c[0:len(c)//2])
    lyrics_part2 = '<br>'.join(c[len(c)//2+1:len(c)])

    message = """<html>
    <head></head>
    <meta http-equiv="refresh" content="5; URL=http://[[[[URL_TO_YOUR_SITE]]]">
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
    </body>
    </html>""".format(page_title, lyrics_part1, lyrics_part2)
    f.write(message)
    f.close()

while True:
    try:
        song_artist, song_title = song_info()
        print("Looking up: {} - {}".format(song_artist, song_title))
        song_lyrics = PyLyrics.PyLyrics.getLyrics(song_artist, song_title)
        generate_output("{} - {}".format(song_artist, song_title), song_lyrics)
        print("Process Successful")

    except ValueError:
        print("Not found")
        pass
    except AttributeError:
        print("No connection")
        pass
    time.sleep(2)

