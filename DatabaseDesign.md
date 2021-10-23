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

```
