import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
    host='localhost',
    user='user',
    database='userdatabase',
    password='**pass**'
    )
mycursor = mydb.cursor()

def create_city_table():
    mycursor.execute("create table City (\
        CityID INT,\
        CityName VARCHAR(100),\
        StateName VARCHAR(50),\
        StateAbbrev VARCHAR(2),\
        Lat DECIMAL(8,6),\
        Lng DECIMAL(9,6),\
        PRIMARY KEY (CityID) );")
def create_route_table():
    mycursor.execute("create table Route (\
        RouteID INT,\
        StartCityID INT,\
        EndCityID INT,\
        TravelTime_min REAL,\
        PRIMARY KEY (RouteID),\
        FOREIGN KEY (StartCityID) REFERENCES City(CityID),\
        FOREIGN KEY (EndCityID) REFERENCES City(CityID) );")
def create_concert_table():
    mycursor.execute("create table Concert (\
        ConcertID INT,\
        CityID INT,\
        ConcertName VARCHAR(100),\
        Date VARCHAR(15),\
        Time VARCHAR(10),\
        Location VARCHAR(100),\
        PRIMARY KEY (ConcertID),\
        FOREIGN KEY (CityID) REFERENCES City(CityID) );")
def create_song_table():
    mycursor.execute("create table Song (\
        SongID INT,\
        CityID INT,\
        SongName VARCHAR(100),\
        ArtistName VARCHAR(100),\
        SpotifyID VARCHAR(30),\
        Duration REAL,\
        PRIMARY KEY (SongID),\
        FOREIGN KEY (CityID) REFERENCES City(CityID) );")

def fill_cities():
    city_entries = pd.read_csv("citytable.csv")
    for i,row in city_entries.iterrows():
        values = str(row['city_id']) + ", '" + str(row['city_name']) + "', '" + str(row['state_name']) + "', '" + str(row['state_abbrev']) + "', " + str(row['lat']) + ", " + str(row['lng'])
        mycursor.execute("insert into City values ("+values+");")
def fill_routes():
    route_entries = pd.read_csv("routetable.csv")
    for i,row in route_entries.iterrows():
        values = str(row[0]) + ", " + str(row['city1']) + ", " + str(row['city2']) + ", " + str(row['travel_time'])
        mycursor.execute("insert into Route values ("+values+");")
def fill_concerts():
    concert_entries = pd.read_csv("concerttable.csv")
    for i,row in concert_entries.iterrows():
        values = str(row['concert_id']) + ", " + str(row['city_id']) + ", '" + str(row['concert_name']) + "', '" + str(row['concert_date']) + "', '" + str(row['concert_time']) + "', '" + str(row['location']) + "'"
        mycursor.execute("insert into Concert values ("+values+");")
def fill_songs():
    song_entries = pd.read_csv("songtable.csv")
    for i,row in song_entries.iterrows():
        values = str(row['song_id']) + ", " + str(row['city_id']) + ", '" + str(row['song_name']) + "', '" + str(row['artist_name']) + "', '" + str(row['spotify_song_id']) + "', " + str(row['duration_s'])
        mycursor.execute("insert into Song values ("+values+");")

def create_all_tables():
    create_city_table()
    create_route_table()
    create_concert_table()
    create_song_table()
def fill_all_tables():
    fill_cities()
    fill_routes()
    fill_concerts()
    fill_songs()

# Tables Created & Filled, shouldn't have to run again
#create_all_tables()
#fill_all_tables()
#mydb.commit()

# Testing filled tables
mycursor.execute('select * from City where CityID = 1;')
print([row for row in mycursor])
mycursor.execute('select * from Route where RouteID = 1;')
print([row for row in mycursor])
mycursor.execute('select * from Concert where ConcertID = 1;')
print([row for row in mycursor])
mycursor.execute('select * from Song where SongID = 1;')
print([row for row in mycursor])
