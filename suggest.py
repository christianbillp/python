from flask import Flask, request
import random
import os

suggestions = ["Cake", "Waterpark", "Cinema"]

['sushi/'+filename for filename in os.listdir('sushi')]

app = Flask(__name__)
@app.route('/')
def get_frontpage():    
    frontpage = """
<img src="sushi/maguro.png />
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

