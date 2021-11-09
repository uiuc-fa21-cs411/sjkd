from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from app.models import db,SongModel
 
app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sajay:%ArtisanSQL01_@localhost:3306/sajay_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
song = db.Table('Song', db.metadata, autoload=True, autoload_with=db.engine)

@app.before_first_request
def create_table():
    db.create_all()
 
@app.route('/data/create' , methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')
 
    if request.method == 'POST':
        SongID = request.form['SongID']
        CityID = request.form['CityID']
        SongName = request.form['SongName']
        SpotifyID = request.form['SpotifyID']
        Duration = request.form['Duration']
        s = SongModel(SongID=SongID, CityID=CityID, SongName=SongName, SpotifyID = SpotifyID, Duration = Duration)
        db.session.add(song)
        db.session.commit()
        return redirect('/data')
 
 
@app.route('/data')
def RetrieveList():
    songs = SongModel.query.all()
    return render_template('datalist.html',songs = songs)
 
 
@app.route('/data/<int:id>')
def RetrieveSong(id):
    song = EmployeeModel.query.filter_by(SongID=id).first()
    if song:
        return render_template('data.html', song = song)
    return f"Song with id = {id} doenst exist"
 
 
@app.route('/data/<int:id>/update',methods = ['GET','POST'])
def update(id):
    song = SongModel.query.filter_by(SongID=id).first()
    if request.method == 'POST':
        if song:
            db.session.delete(song)
            db.session.commit()
            CityID = request.form['CityID']
            SongName = request.form['SongName']
            SpotifyID = request.form['SpotifyID']
            Duration = request.form['Duration']
            song = SongModel(SongID=SongID, CityID=CityID, SongName=SongName, SpotifyID = SpotifyID, Duration = Duration)
            db.session.add(song)
            db.session.commit()
            return redirect(f'/data/{id}')
        return f"Song with id = {id} Does nit exist"
 
    return render_template('update.html', employee = employee)
 
 
@app.route('/data/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    song = SongModel.query.filter_by(song_id=id).first()
    if request.method == 'POST':
        if song:
            db.session.delete(song)
            db.session.commit()
            return redirect('/data')
        abort(404)
 
    return render_template('delete.html')
 
app.run(host='localhost', port=5000)