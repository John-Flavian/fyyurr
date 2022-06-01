import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()



class Venues(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(400))
    genres = db.Column(db.ARRAY(db.String()))
    seeking_talent = db.Column(db.Boolean(), nullable=False, default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Shows', backref='venue', lazy=True)
# This allows us to print our data in python interactive mode

    def __repr__(self):
        return f'<Venues {self.id} {self.name}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artists(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(500))
    seeking_description = db.Column(db.String(400))
    seeking_venue = db.Column(db.Boolean(), nullable=False, default=False)
    website_link = db.Column(db.String(500))
    shows = db.relationship('Shows', backref='artist', lazy=True)
# This allows us to print our data in python interactive mode
    def __repr__(self):
        return f'<Artists {self.id} {self.name}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate



class Shows(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)
    start_time = db.Column(db.DateTime(), default=datetime.datetime.utcnow(), nullable=False)
    # This allows us to print our data in python interactive mode
    def __repr__(self):
      return f'<Shows {self.id} {self.venue_id} {self.artist_id} {self.start_time}>'
