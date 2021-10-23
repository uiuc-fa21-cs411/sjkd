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
