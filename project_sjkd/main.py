from datetime import date
import math
import mysql.connector
import pandas as pd
from flask import Flask, render_template, make_response
from flask import redirect, request, jsonify, url_for
from flask import stream_with_context, Response
from datetime import date

host = '0.0.0.0'
port = '10036'

user = 'test_user'
playlist_count = 0
app = Flask(__name__)

mydb = mysql.connector.connect(
    host='localhost',
    user='sajay',
    database='sajay_database',
    password='%ArtisanSQL01_'
    )
mycursor = mydb.cursor()

### Helper Functions ###
def get_roadtrip_len(city1, city2):
    time_query = f'\
        select TravelTime_min \
        from Route \
        where (StartCityID = {city1} and EndCityID = {city2}) \
            or (StartCityID = {city2} and EndCityID = {city1})'
    mycursor.execute(time_query)
    result = mycursor.fetchall()
    if (len(result) <= 0):
        return render_template('display_playlist.html', title="Could not create playlist", playlist=[])
    route_time_min = result[0][0]
    return route_time_min

def generate_playlist(start, end, trip_time):
    song_query_start = '\
        select SongName, ArtistName, Song.Duration, CityName \
        from Song inner join City on Song.CityID = City.CityID \
        where City.CityID = '
    song_query_end = ' order by SongID'
    
    # Fill up to half of the road trip with one city's songs
    playlist = []
    playlist_time_min = 0
    mycursor.execute(song_query_start + start + song_query_end)
    for row in mycursor.fetchall():
        if (playlist_time_min >= trip_time / 2):
            break
        playlist.append(row)
        playlist_time_min += row[2] / 60 + 1
    print(playlist_time_min)
    
    mycursor.execute(song_query_start + end + song_query_end)
    for row in mycursor.fetchall():
        if (playlist_time_min >= trip_time):
            break
        playlist.append(row)
        playlist_time_min += row[2] / 60 + 1
    print(playlist_time_min)
    return playlist, playlist_time_min

def get_concert_list(city):
    today = date.today().strftime("%m/%d/%y")
    mycursor.execute(f'\
        select Date, Time, ConcertName, Location \
        from Concert \
        where Date >= {today} and CityID = {city} \
        limit 5')
    return mycursor.fetchall()

### Routing Functions ###
@app.route('/')
def index():
    title = 'Roadtrip Playlist Generator'
    playlist_count = 1

    mycursor.execute('\
        select CityName, City.CityID, COUNT(SongID) \
        from City inner join Song on City.CityID = Song.CityID \
        group by City.CityID \
        having COUNT(SongID) > 0 ')
    cities_list = [str(row[1]) + ': ' + str(row[0]) for row in mycursor]

    return render_template('starting_city.html', title=title, cities_list=cities_list)

@app.route('/from/<starting_city>')
def enter_end(starting_city):
    title = 'Roadtrip Playlist Generator'
    srcID, _ = str(starting_city).split(": ")

    mycursor.execute('\
        select CityName, City.CityID, COUNT(SongID) \
        from City inner join Song on City.CityID = Song.CityID \
        where City.CityID != '+srcID+' \
        group by City.CityID \
        having COUNT(SongID) > 0 ')
    cities_list = [str(row[1]) + ': ' + str(row[0]) for row in mycursor]

    return render_template('ending_city.html', title=title, src=starting_city, cities_list=cities_list)

@app.route('/add/playlist/<starting_city>/<ending_city>')
def add_playlist(starting_city, ending_city):
    srcID, _ = str(starting_city).split(": ")
    destID, _ = str(ending_city).split(": ")

    select = f'\
        select COUNT(PlaylistID) \
        from Playlist \
        where User like \"{user}\" \
        group by User'
    mycursor.execute(select)
    playlist_count = mycursor.fetchall()
    print(playlist_count)
    if (len(playlist_count) <= 0):
        new_id = 0
    else:
        new_id = playlist_count[0][0] + 1

    insert = f'\
        insert into Playlist \
        values ({new_id}, \'{user}\', \'{srcID}\', \'{destID}\')'
    mycursor.execute(insert)

    return redirect(url_for('generate_playlist_concerts', starting_city=starting_city, ending_city=ending_city))

@app.route('/delete/playlist/<playlistID>')
def delete_playlist(playlistID):
    delete = f'DELETE FROM Playlist WHERE PlaylistID = {playlistID};'
    mycursor.execute(delete)

    select = 'SELECT * FROM Playlist ORDER BY PlaylistID DESC LIMIT 1;'
    mycursor.execute(select)
    temp = mycursor.fetchall()

    for pid in range(temp[0][1] + 1):
        if (pid > int(playlistID)):
            update = f'UPDATE Playlist SET PlaylistID = PlaylistID - 1 WHERE PlaylistID = {pid};'
            mycursor.execute(update)

    return redirect(url_for('show_my_playlists'))

@app.route('/from/<starting_city>/to/<ending_city>')
def generate_playlist_concerts(starting_city, ending_city):
    srcID, src = str(starting_city).split(": ")
    destID, dest = str(ending_city).split(": ")
    print(src)
    print(dest)

    roadtrip_time = get_roadtrip_len(srcID, destID)
    playlist,playlist_time_min = generate_playlist(srcID, destID, roadtrip_time)
    concert_list = get_concert_list(destID)

    return render_template('display_playlist.html', start=src, end=dest, playlist=playlist, time=int(playlist_time_min), concerts=concert_list)

@app.route('/myplaylists')
def show_my_playlists():
    title = 'Roadtrip Playlist Generator'

    mycursor.execute('select * from Playlist')
    playlist = mycursor.fetchall()

    return render_template('my_playlists.html', title=title, playlist=playlist)

if __name__ == '__main__':
    app.run(port=port)
