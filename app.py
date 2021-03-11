#! /usr/bin/env python
import os
from base64 import b64encode
from urllib.parse import urlencode

import requests
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route("/ping")
def ping():
    """ health check """
    return "pong"


@app.route("/docs/<pdf>")
def doc(pdf):
    """ api to retrieve pdf documents as base64 encoded strings """
    with open(f"./docs/{pdf}", "rb") as f:
        data = f.read()
        data = b64encode(data).decode("utf-8")
    return f"data:application/pdf;base64,{data}"


@app.route("/youtube/<channel>")
def youtube(channel):
    """ api to retrieve latest videos of the channel specified """
    params = urlencode({
        "key": os.environ["API_KEY"],
        "part": "snippet",
        "order": "date",
        "maxResults": 25,
        "channelId": channel,
    })
    url = f"https://youtube.googleapis.com/youtube/v3/search?{params}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    """ run the flask server """
    port = os.getenv("PORT", 5000)
    app.run(host="0.0.0.0", port=port)
