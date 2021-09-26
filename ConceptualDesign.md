# Conceptual and Logical Database Design

## ER / UML Diagram
<p align="center">
<img src="ERUML.jpg" width="400"/>
</p>

## Logical Design (Relational Schema)
- __CityPlaylist__(
CityPlaylistID: int [PK],
CityID: int [FK to City.CityID],
AppleMusicID: int 
);
- __Song__(
SongID:int [PK],
Name: varchar(64),
SongLength: real
);
- __City__(
CityID:int [PK],
CityPlaylistID:int [FK to CityPlaylist.CityPlaylistID],
Name:varchar(64)
);
- __Route__(
RouteID:int [PK],
StartLocation:varchar(64),
EndLocation:varchar(64)
);
- __User__(
UserID:int [PK],
FirstName:varchar(64)
);

- __FinalPlaylist__(
PlaylistID:int [PK],
PlaylistLength int
UserID: int [FK to User.UserID]
);
- __CitiesNearby__(
CityID:int [FK to City.CityID],
RouteID:int [FK to Route.RouteID],
TimeToNext:int 
CityCount:int
);

- __CityPlaylistSongs__(
CityPlaylistID:int [FK to CityPlaylist.CityPlaylistID],
SongID:int [FK to Song.SongID]
);
- __UserRoute__(
RouteID: int [FK to Route.RouteID],
UserID: int [FK to User.UserID]
);
- __FinalPlaylistSongs__(
SongID: int [FK to Song.SongID],
FinalPlaylistID: int [FK to FinalPlaylist.FinalPlaylistID]
);