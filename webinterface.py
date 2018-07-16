'''
#%% Web interface example
#   This example shows how to host a webservice with an input box
from flask import Flask, request

app = Flask(__name__)
@app.route('/')
def get_frontpage():
    frontpage = """
    <h1>Headline</h1>
    <form method="POST">
        <textarea name="text" cols="20" rows="3"></textarea>
        <br>
        <input type="submit" value="Set Value">
    </form>"""

    return frontpage

@app.route('/', methods=['POST'])
def return_results():
    text = request.form['text']

    print(text)

    return f'You have entered {text}'

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80)
    
'''

from flask import Flask, request
import random
import os

suggestions = ["Cake", "Waterpark", "Cinema"]

['sushi/'+filename for filename in os.listdir('sushi')]

app = Flask(__name__)
@app.route('/')
def get_frontpage():    
    frontpage = f"""

What about...
<img src="sushi/maguro.png />
{random.choice(suggestions)}

"""
    return frontpage

@app.route('/', methods=['POST'])
def return_results():
    text = request.form['text']

    print(text)   # This is where the magic happens! This is what the variable is used for

    return 'It works'

print(get_frontpage())

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80)
    