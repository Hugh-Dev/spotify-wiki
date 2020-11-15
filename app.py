# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, request, make_response, Response, jsonify
from flask.views import View
import json
from pymongo import MongoClient
from bson import ObjectId
import pymongo
from datetime import date, datetime
import pprint
from bson.json_util import dumps
import sys
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import wikipedia

wikipedia.set_lang("es")
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def Index():
    class Spotify:
        def __init__(self, arg):
            self.df = pd.read_csv(arg)
            self.df = self.df.query('track_popularity == 0')
        
        def duplicados(self):
            df = self.df
            self.verifica = df['track_id'].duplicated()
            for i in self.verifica:
                if i == True:
                    df = df.drop_duplicates(subset='track_id', keep='last')
            return df

    spy = Spotify('spotify_songs.csv')
    limpio = spy.duplicados()
    artist = limpio['track_artist']
    artist = artist.drop_duplicates()
    return render_template('template.index.html', artist=artist)

@app.route('/artist', methods=['GET', 'POST'])
def Artist():
    if request.method == 'POST':
        class Wiki:
            def summary(self, arg):
                try:
                    self.artist = arg
                    summary = wikipedia.summary(self.artist)
                    return summary
                except Exception as e:
                    msg = '404'
                    return msg


        choosename = request.form["choosename"]
        w = Wiki()
        wiki = w.summary(choosename)

        return render_template('template.wiki.html', summary=wiki)



if __name__ == '__main__':
    app.run(debug=True)
