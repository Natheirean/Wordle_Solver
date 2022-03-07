from crypt import methods
from distutils.log import debug
from urllib import request
from flask import request
from flask import Flask, render_template, redirect
import json
import algo
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/guess')
def make_guess():
    output = request.get_json()
    print(output)  # This is the output that was stored in the JSON within the browser
    print(type(output))

    # this converts the json output to a python dictionary
    result = json.loads(output)
    print(result)  # Printing the new dictionary
    print(type(result))  # this shows the json converted as a python dictionary
    return result


if __name__ == "__main__":
    app.run(debug=True)
