# Database Design
## DDL
```
CREATE TABLE City (
    CityID INT,
    CityName VARCHAR(100),
    StateName VARCHAR(50),
    StateAbbrev VARCHAR(2),
    Lat DECIMAL(8,6),
    Lng DECIMAL(9,6),
    PRIMARY KEY (CityID)
);

CREATE TABLE Route (
    RouteID INT,
    StartCityID INT,
    EndCityID INT,
    TravelTime_min REAL,
    PRIMARY KEY (RouteID),
    FOREIGN KEY (StartCityID) REFERENCES City(CityID),
    FOREIGN KEY (EndCityID) REFERENCES City(CityID)
);

CREATE TABLE Concert (
    ConcertID INT,
    CityID INT,
    ConcertName VARCHAR(100),
    Date VARCHAR(15),
    Time VARCHAR(10),
    Location VARCHAR(100),
    PRIMARY KEY (ConcertID),
    FOREIGN KEY (CityID) REFERENCES City(CityID)
);

CREATE TABLE Song (
    SongID INT,
    CityID INT,
    SongName VARCHAR(100),
    ArtistName VARCHAR(100),
    SpotifyID VARCHAR(30),
    Duration REAL,
    PRIMARY KEY (SongID),
    FOREIGN KEY (CityID) REFERENCES City(CityID)
);
```
## Data Tables 
[Songs Table](https://github.com/uiuc-fa21-cs411/sjkd/blob/main/tables/songtable.csv)
[Cities Table](https://github.com/uiuc-fa21-cs411/sjkd/blob/main/tables/citytable.csv)
[Routes Table](https://github.com/uiuc-fa21-cs411/sjkd/blob/main/tables/routetable.csv)
[Concerts Table](https://github.com/uiuc-fa21-cs411/sjkd/blob/main/tables/concerttable.csv)

## Advanced Query 1
```
Query 1 EXPLAIN ANALYZE output without indexing:

[("-> Filter: (numConcerts >= 3)  (actual time=1.125..1.128 rows=14 loops=1)\n    
-> Table scan on <temporary>  (actual time=0.001..0.002 rows=14 loops=1)\n       
 -> Aggregate using temporary table  (actual time=1.124..1.125 rows=14 loops=1)\n           
 -> Nested loop inner join  (cost=159.75 rows=42) (actual time=0.084..0.965 rows=85 loops=1)\n               
 -> Filter: (Concert.`Date` like '%/2022')  (cost=115.65 rows=126) (actual time=0.063..0.583 rows=283 loops=1)\n                    
-> Table scan on Concert  (cost=115.65 rows=1134) (actual time=0.060..0.334 rows=1134 loops=1)\n                
-> Filter: (City.Lng > -90.000000)  (cost=0.25 rows=0) (actual time=0.001..0.001 rows=0 loops=283)\n                    
-> Single-row index lookup on City using PRIMARY (CityID=Concert.CityID)  (cost=0.25 rows=1) (actual time=0.001..0.001 rows=1 loops=283)\n",)]

Total time: 4.139 ms

```

## Advanced Query 2

```
Query 2 EXPLAIN ANALYZE output without indexing:

('-> Sort: `count(Song.CityID)` DESC  (actual time=1.467..1.469 rows=15 loops=1)\n   
 -> Filter: (count(Song.CityID) >= 7)  (actual time=0.962..1.451 rows=15 loops=1)\n       
 -> Stream results  (cost=1189.55 rows=2156) (actual time=0.961..1.445 rows=43 loops=1)\n            -> Group aggregate: count(Song.CityID), count(Song.CityID)  (cost=1189.55 rows=2156) (actual time=0.956..1.422 rows=43 loops=1)\n                
-> Nested loop inner join  (cost=973.95 rows=2156) (actual time=0.088..1.231 rows=2156 loops=1)\n                    
-> Filter: (Song.CityID is not null)  (cost=219.35 rows=2156) (actual time=0.076..0.680 rows=2156 loops=1)\n                        
-> Index scan on Song using CityID  (cost=219.35 rows=2156) (actual time=0.074..0.561 rows=2156 loops=1)\n                    
-> Single-row index lookup on City using PRIMARY (CityID=Song.CityID)  (cost=0.25 rows=1) (actual time=0.000..0.000 rows=1 loops=2156)\n',)

Total time: 8.259
```

### Indexing
[Outputs and Analysis](https://docs.google.com/document/d/1H-vxBEzS4skHhmzbkW2LONUZ39-DrrFnIGNI5PnBo-A/edit?usp=sharing)
