import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
    host='localhost',
    user='user',
    database='user_database',
    password='**pass**'
    )
mycursor = mydb.cursor()

# Advanced Query 1:
# Find the number of concerts in 2022 on the east side of the United 
# States. Return the name of the city and state, and the concert count
# for each. Only return cities with at least 3 concerts.
def query1():
    print("-------------------- Query 1 --------------------")
    mycursor.execute('CREATE INDEX state_name_index ON City (CityName(5)) USING HASH;')
    mycursor.execute('EXPLAIN ANALYZE SELECT CityName, StateName, count(Concert.ConcertID) as numConcerts\
                      FROM Concert \
                      LEFT JOIN City on Concert.CityID = City.CityID\
                      WHERE Lng > -90 and Date like \"%/2022\"\
                      GROUP by CityName, StateName\
                      HAVING numConcerts >= 3;')
    for row in mycursor:
        print(row)
        times = [str(row)[i+2:i+7] for i in find_all('..', str(row))]
        results = [float(i) for i in times]
        print(sum(results))
    mycursor.execute('DROP INDEX state_name_index ON City')
# SELECT CityName, StateName, count(Concert.ConcertID) as numConcerts FROM Concert  LEFT JOIN City on Concert.CityID = City.CityID WHERE Lng > -95 and Date like "%/2022" GROUP by CityName, StateName HAVING numConcerts >= 3;

# Advanced Query 2
# List all cities which have more than 7 songs written about them.
# Return the city_id, city_name, state_name, and the number of songs.
# Order the results by the number of songs per city in descending order
def query2():
    print("-------------------- Query 2 --------------------")
    mycursor.execute('CREATE INDEX state_name_index ON City (CityName(5)) USING BTREE;')
    mycursor.execute('EXPLAIN ANALYZE SELECT Song.CityID, CityName, StateName, count(Song.CityID)\
                      FROM Song\
                      INNER JOIN City on City.CityID = Song.CityID\
                      GROUP by Song.CityID\
                      HAVING count(Song.CityID) >= 7\
                      ORDER by count(Song.CityID) DESC;')
    for row in mycursor:
        print(row)
        times = [str(row)[i+2:i+7] for i in find_all('..', str(row))]
        results = [float(i) for i in times]
        print(sum(results))
    mycursor.execute('DROP INDEX state_name_index ON City')
# SELECT Song.CityID, CityName, StateName, count(Song.CityID) FROM Song INNER JOIN City on City.CityID = Song.CityID GROUP by Song.CityID HAVING count(Song.CityID) >= 7 ORDER by count(Song.CityID) DESC;


#HELPER FUNCTION TO SUM QUERY TIME
def find_all(sub, str):
    idx = str.find(sub)
    while idx != -1:
        yield idx
        idx = str.find(sub, idx+1)
    
query2()


