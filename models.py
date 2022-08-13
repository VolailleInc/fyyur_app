#**********Imported Libraries*********#

from flask import Flask
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#*******Application Configuration******#
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app,db)

#*************Database Models************#
class Venue_table(db.Model):
    __tablename__ = 'Venue_table'

    venue_id = db.Column(db.Integer, primary_key=True)
    venue_name = db.Column(db.String, nullable=False)
    venue_phone = db.Column(db.String(120))
    venue_address = db.Column(db.String(120), nullable=False)
    venue_city = db.Column(db.String(120), nullable=False)
    venue_state = db.Column(db.String(120), nullable=False)
    venue_image_link = db.Column(db.String(500))
    genres_at_venue = db.Column("genres_at_venue", db.ARRAY(db.String()), nullable=False)
    venue_facebook_link = db.Column(db.String(120))
    venue_website = db.Column(db.String(250))
    venue_seeking_talent = db.Column(db.Boolean, default=True)
    venue_seeking_description = db.Column(db.String(250))
    shows = db.relationship('Show', backref='venue', lazy=True)

    def __repr__(self):
      return f'<Venue: {self.venue_id} name: {self.venue_name}>'


class Artist_table(db.Model):
    __tablename__ = 'Artist_table'

    artist_id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String, nullable=False)
    artist_city = db.Column(db.String(120), nullable=False)
    artist_state = db.Column(db.String(120), nullable=False)
    artist_phone = db.Column(db.String(120))
    artist_genres = db.Column("artist_genres", db.ARRAY(db.String()), nullable=False)
    artist_image_link = db.Column(db.String(500))
    artist_facebook_link = db.Column(db.String(120))
    shows = db.relationship('Show', backref='artist', lazy=True)

    def __repr__(self):
      return f'<ArtistID: {self.artist_id} name: {self.artist_name}>'


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
      return f'<Show {self.id}, Artist {self.artist_id}, Venue {self.venue_id}>'
