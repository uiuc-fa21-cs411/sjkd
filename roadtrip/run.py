from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sajay:%ArtisanSQL01_@localhost:3306/sajay_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

song = db.Table('Song', db.metadata, autoload=True, autoload_with=db.engine)

@app.route('/')
def index():
    songs = db.session.query(song).all()
    return render_template('datafile.html', songs = songs, length = len(songs))

app.run(host='localhost', port=5000)