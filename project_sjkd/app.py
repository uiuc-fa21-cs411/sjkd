import math
import sqlite3
import pandas
from flask import Flask, render_template, make_response
from flask import redirect, request, jsonify, url_for
from flask import stream_with_context, Response

host = '20.88.14.242'
port = '10038'

sqlite_uri = 'roadtrip.db'
row_limit = 1000
app = Flask(__name__)

songs_length = 10


@app.route('/', methods=['GET'])
def index():
    title = 'Roadtrip Project'
    return render_template('index.html', title=title)

@app.route('/create', methods=['GET'])
def createForm():
    df = pandas.read_csv('data/songtable.csv', index_col = 0)
    cols = df.columns
    title = 'Create a new entry in the song table'
    return render_template('create.html', title=title, columns= cols)

@app.route('/create', methods=['POST'])
def create():
    con = sqlite3.connect(sqlite_uri)
    cur = con.cursor()
    songs_length = con.execute("select count(*) from songs").fetchone()[0]

    new_entry = (songs_length,) + tuple((str(request.form['input']).split(',')))
    sql = "INSERT INTO songs(song_id,song_name,artist_name,city_id,spotify_song_id,duration_s) VALUES"
    sql += str(new_entry)
    con.execute(sql)
    con.commit()
    con.close()
    return ''

@app.route('/delete', methods=['GET'])
def deleteForm():
    cols = ['song_id']
    title = 'Remove an entry from the song table'
    return render_template('delete.html', title=title, columns= cols)

@app.route('/delete', methods=['POST'])
def delete():
    con = sqlite3.connect(sqlite_uri)
    cur = con.cursor()
    songs_length = con.execute("select count(*) from songs").fetchone()[0]

    s_id = str(request.form['input'])
    if int(s_id) < songs_length:
        sql = 'DELETE FROM songs WHERE song_id=' + str(s_id)
        con.execute(sql)
        con.commit()
        con.close()
    return ''


@app.route('/update', methods=['GET'])
def updateForm():
    df = pandas.read_csv('data/songtable.csv')
    cols = df.columns
    title = 'Update an entry in the song table'
    return render_template('update.html', title=title, columns= cols)

@app.route('/update', methods=['POST'])
def update():
    cols = pandas.read_csv('data/songtable.csv').columns
    con = sqlite3.connect(sqlite_uri)
    cur = con.cursor()
    songs_length = con.execute("select count(*) from songs").fetchone()[0]

    new_entry = tuple((str(request.form['input']).split(',')))
    print(new_entry)
    s_id = str(new_entry[0])
    if int(s_id) < songs_length:
        sql = "UPDATE songs SET "
        for i in range(1, len(new_entry)):
            if new_entry[i]:
                sql += str(cols[i] + " = '" + new_entry[i] + "',")
        sql = sql[:-1]
        sql += " WHERE song_id = " + str(s_id)
        print(sql)
        con.execute(sql)
        con.commit()
        con.close()
    return ''

@app.route('/search', methods=['GET'])
def search():
    title = 'Search for a keyword'
    return render_template('search.html', title=title)

@app.route('/query', methods=['GET'])
def query():
    title = 'Query the Database'
    return render_template('query.html', title=title)


@app.route('/query', methods=['POST'])
def process_query():
    sql = request.form['query_string']
    print(sql)
    con = sqlite3.connect(sqlite_uri)
    df = pandas.read_sql_query(sql, con).head(row_limit)
    con.close()

    def make_valid(v):
        if v != v:
            return None
        else:
            return v

    column_labels = [col for col in df.columns]
    per_col_values = [
        [make_valid(value) for value in df[col]]
        for col in df.columns
    ]

    response = {
        "query_string": sql,
        "data": {
            "labels": [[col] for col in column_labels],
            "values": per_col_values
        }
    }

    return response

def insert_into_sqlite(csvfile, name):
    con = sqlite3.connect(sqlite_uri)
    cur = con.cursor()
    df = pandas.read_csv(csvfile)
    df.to_sql(name, con, if_exists='replace', index=False)
    con.commit()
    con.close()


if __name__ == '__main__':
    insert_into_sqlite('data/songtable.csv', 'songs')
    insert_into_sqlite('data/concerttable.csv', 'concerts')
    insert_into_sqlite('data/routetable.csv', 'routes')
    insert_into_sqlite('data/citytable.csv', 'cities')
    insert_into_sqlite('data/songtable(full).csv', 'songs2')
    app.run(port=port)
