import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='kes8',
    database='kes8_database',
    password='TrackRail21!'
    )
mycursor = mydb.cursor()

mycursor.execute("create table City (CityID INT, CityName VARCHAR(100), StateName VARCHAR(50), StateAbbrev VARCHAR(2), Lat DECIMAL(8,6), Lng DECIMAL(9,6), PRIMARY KEY (CityID) );")
mycursor.execute("create table Route (RouteID INT, StartCityID INT, EndCityID INT, TravelTime_min REAL, PRIMARY KEY (RouteID), FOREIGN KEY (StartCityID) REFERENCES City(CityID), FOREIGN KEY (EndCityID) REFERENCES City(CityID) );")
mycursor.execute("create table Concert (ConcertID INT, CityID INT, ConcertName VARCHAR(100), Date VARCHAR(15), Time VARCHAR(10), Location VARCHAR(100), PRIMARY KEY (ConcertID), FOREIGN KEY (CityID) REFERENCES City(CityID) );")
mycursor.execute("create table Song (SongID INT, CityID INT, SongName VARCHAR(100), ArtistName VARCHAR(100), SpotifyID VARCHAR(30), Duration REAL, PRIMARY KEY (SongID), FOREIGN KEY (CityID) REFERENCES City(CityID) );")

mycursor.execute('select * from City where CityID = 1;')
print([row for row in mycursor])