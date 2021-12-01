import math
import mysql.connector
import pandas as pd
from flask import Flask, render_template, make_response
from flask import redirect, request, jsonify, url_for
from flask import stream_with_context, Response

host = '20.88.14.242'
port = '10038'

src = ''
dest = ''
app = Flask(__name__)

mydb = mysql.connector.connect(
    host='localhost',
    user='sajay',
    database='sajay_database',
    password='%ArtisanSQL01_'
    )
mycursor = mydb.cursor()

@app.route('/')
def index():
    title = 'Roadtrip Playlist Generator'

    mycursor.execute('select CityName, CityID from City')
    cities_list = [row[0] for row in mycursor]

    return render_template('starting_city.html', title=title, cities_list=cities_list)

@app.route('/from/<starting_city>')
def enter_end(starting_city):
    src = str(starting_city)
    title = 'Roadtrip Playlist Generator'

    mycursor.execute('select CityName, CityID from City')
    cities_list = [row[0] for row in mycursor]

    return render_template('ending_city.html', title=title, src=starting_city, cities_list=cities_list)

@app.route('/from/<starting_city>/to/<ending_city>')
def generate_playlist(starting_city, ending_city):
    src = str(starting_city)
    dest = str(ending_city)
    print(src)
    print(dest)
    title = 'Roadtrip Playlist Generator'

    mycursor.execute('select * from Song')
    playlist = mycursor.fetchall()

    return render_template('display_playlist.html', title=title, playlist=playlist)

@app.route('/myplaylists')
def show_my_playlists():
    title = 'Roadtrip Playlist Generator'

    mycursor.execute('select * from Song')
    playlist = mycursor.fetchall()

    return render_template('display_playlist.html', title=title, playlist=playlist)


if __name__ == '__main__':
    app.run(port=port)
