from datetime import date, time
import math
import mysql.connector
import pandas as pd
from flask import Flask, render_template, make_response
from flask import redirect, request, jsonify, url_for
from flask import stream_with_context, Response
from datetime import date

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

### Helper Functions ###
def create_procedure():
    procedure = '\
        create procedure generate_playlist_concerts(IN src INT, IN dest INT, IN select_flag VARCHAR(10), IN today VARCHAR(15), OUT playlist_time INT) \
        begin \
            set playlist_time = 0; \
            if (select_flag = \"playlist\") then \
                select SongName, ArtistName, Song.Duration, CityName \
                from Song inner join City on Song.CityID = City.CityID \
                where City.CityID = src \
                order by SongID; \
                select SongName, ArtistName, Song.Duration, CityName \
                from Song inner join City on Song.CityID = City.CityID \
                where City.CityID = dest \
                order by SongID; \
            else \
                select Date, Time, ConcertName, Location \
                from Concert \
                where Date >= today and CityID = dest \
                order by ConcertID \
                limit 5; \
            end if; \
        end'
    mycursor.execute(procedure)

def delete_procedure():
    mycursor.execute('drop procedure if exists generate_playlist_concerts')

def exec_procedure(start, end, selection):
    today = date.today().strftime("%m/%d/%y")
    print("Running Procedure")
    args = mycursor.callproc('generate_playlist_concerts', (start, end, selection, today, None))
    print("Procedure done")

    playlist_time = args[4]
    print(playlist_time)
    
    selection = []
    for result in mycursor.stored_results():
        selection.append(row for row in result.fetchall())
    
    return selection, playlist_time

### Routing Functions ###
@app.route('/')
def index():
    title = 'Roadtrip Playlist Generator'
    playlist_count = 1

    mycursor.execute('select * from Playlist')
    playlist = mycursor.fetchall()

    return render_template('my_playlists.html', title=title, playlist=playlist)

@app.route('/from/')
def enter_start():
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
    if (len(playlist_count) <= 0):
        new_id = 0
    else:
        new_id = playlist_count[0][0]

    insert = f'insert into Playlist \
        values ({new_id}, \'{user}\', \'{starting_city}\', \'{ending_city}\');'
    mycursor.execute(insert)
    return redirect(url_for('generate_playlist_concerts', starting_city=starting_city, ending_city=ending_city))

@app.route('/delete/playlist/<playlistID>')
def delete_playlist(playlistID):
    delete = f'DELETE FROM Playlist WHERE PlaylistID = {playlistID};'
    mycursor.execute(delete)

    select = 'SELECT * FROM Playlist ORDER BY PlaylistID DESC LIMIT 1;'
    mycursor.execute(select)
    temp = mycursor.fetchall()
    if (temp):
        for pid in range(temp[0][0] + 1):
            if (pid > int(playlistID)):
                update = f'UPDATE Playlist SET PlaylistID = PlaylistID - 1 WHERE PlaylistID = {pid};'
                mycursor.execute(update)

    return redirect(url_for('show_my_playlists'))

@app.route('/from/<starting_city>/to/<ending_city>')
def generate_playlist_concerts(starting_city, ending_city):
    srcID, src = str(starting_city).split(": ")
    destID, dest = str(ending_city).split(": ")

    playlist, roadtrip_time = exec_procedure(srcID, destID, 'playlist')
    concert_list, _ = exec_procedure(srcID, destID, 'concerts')

    return render_template('display_playlist.html', start=src, end=dest, playlist=playlist, time=int(roadtrip_time), concerts=concert_list)

@app.route('/myplaylists')
def show_my_playlists():
    title = 'Roadtrip Playlist Generator'

    mycursor.execute('select * from Playlist')
    playlist = mycursor.fetchall()

    return render_template('my_playlists.html', title=title, playlist=playlist)

if __name__ == '__main__':
    delete_procedure()
    create_procedure()
    app.run(port=port)
