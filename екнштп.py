import flask
import requests
from flask import request
app = flask.Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def haha():
    print(request.args)
    return "1"


app.run("127.0.0.1", port=80, debug=True)

