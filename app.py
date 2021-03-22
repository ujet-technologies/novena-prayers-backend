#! /usr/bin/env python
import os
from base64 import b64encode
from urllib.parse import urlencode

import requests
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route("/ping")
def ping():
    """ health check api """
    return "pong"


@app.route("/docs/<path:filename>")
def docs(filename):
    """ serve docs from folder """
    return send_from_directory("docs", filename, as_attachment=True)


@app.route("/channels/<channel>")
def youtube(channel):
    """ retrieve latest videos of the given youtube channel """

    # fetch upload playlist
    params = urlencode({
        "id": channel,
        "key": os.environ["API_KEY"],
        "part": "contentDetails",
        
    })
    url = f"https://youtube.googleapis.com/youtube/v3/channels?{params}"
    response = requests.get(url)
    response.raise_for_status()
    response = response.json()

    # fetch playlist
    params = urlencode({
        "key": os.environ["API_KEY"],
        "part": "snippet",
        "maxResults": "50",
        "playlistId": response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"],
        
    })
    url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?{params}"
    response = requests.get(url)
    response.raise_for_status()
    response = response.json()

    return jsonify(response)


if __name__ == "__main__":
    """ run the flask server """
    port = os.getenv("PORT", 5000)
    app.run(host="0.0.0.0", port=port)
