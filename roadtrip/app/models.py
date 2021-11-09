from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()
 
class SongModel(db.Model):
    __tablename__ = "Song"
 
    SongID = db.Column(db.Integer(), primary_key=True)
    CityID = db.Column(db.Integer())
    SongName = db.Column(db.String())
    SpotifyID = db.Column(db.String())
    Duration = db.Column(db.Integer())
 
    def __init__(self, SongID,CityID,SongName,SpotifyID, Duration):
        self.SongID = SongID
        self.CityID = CityID
        self.SongName = SongName
        self.SpotifyID = SpotifyID
        self.Duration = Duration
 
    def __repr__(self):
        return f"{self.SongID}:{self.SongName} - {self.CityID}"