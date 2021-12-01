import math
import mysql.connector
import pandas as pd
from flask import Flask, render_template, make_response
from flask import redirect, request, jsonify, url_for
from flask import stream_with_context, Response

host = '0.0.0.0'
port = '10038'

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
    srcID, src = str(starting_city).split(": ")
    destID, dest = str(ending_city).split(": ")

    select = 'SELECT * FROM Playlist ORDER BY PlaylistID DESC LIMIT 1;'
    mycursor.execute(select)
    temp = mycursor.fetchall()
    print(temp)
    if (temp != []):
        playlist_count = temp[0][1] + 1
    else:
        playlist_count = 0

    insert = f'insert into Playlist values (\'{user}\', {playlist_count}, \'{starting_city}\', \'{ending_city}\');'
    mycursor.execute(insert)

    return redirect(url_for('generate_playlist', starting_city=starting_city, ending_city=ending_city))

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
def generate_playlist(starting_city, ending_city):
    
    srcID, src = str(starting_city).split(": ")
    destID, dest = str(ending_city).split(": ")
    title = 'Roadtrip Playlist Generator'
    print(src)
    print(dest)

    title = 'Roadtrip Playlist Generator'

    # Get trip time length
    time_query = '\
        select TravelTime_min \
        from Route \
        where (StartCityID = '+srcID+' and EndCityID = '+destID+') \
            or (StartCityID = '+destID+' and EndCityID = '+srcID+')'
    mycursor.execute(time_query)
    result = mycursor.fetchall()
    if (len(result) <= 0):
        return render_template('display_playlist.html', title="Could not create playlist", playlist=[])
    route_time_min = result[0][0]
    print(route_time_min)

    # Get songs from each city
    # Fill up to half of the road trip with one city's songs
    song_query_start = '\
        select SongName, ArtistName, Song.Duration, CityName \
        from Song inner join City on Song.CityID = City.CityID \
        where City.CityID = '
    song_query_end = ' order by SongID'
    
    playlist = []
    playlist_time_min = 0
    mycursor.execute(song_query_start + srcID + song_query_end)
    for row in mycursor.fetchall():
        if (playlist_time_min >= route_time_min / 2):
            break
        playlist.append(row)
        playlist_time_min += row[2] / 60 + 1
    print(playlist_time_min)
    
    mycursor.execute(song_query_start + destID + song_query_end)
    for row in mycursor.fetchall():
        if (playlist_time_min >= route_time_min):
            break
        playlist.append(row)
        playlist_time_min += row[2] / 60 + 1
    print(playlist_time_min)

    return render_template('display_playlist.html', title=title, playlist=playlist)

@app.route('/myplaylists')
def show_my_playlists():
    title = 'Roadtrip Playlist Generator'

    mycursor.execute('select * from Playlist')
    playlist = mycursor.fetchall()

    return render_template('my_playlists.html', title=title, playlist=playlist)


if __name__ == '__main__':
    mycursor.execute("DELETE FROM Playlist;")
    app.run(port=port)
