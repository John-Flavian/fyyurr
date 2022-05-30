#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
from re import A
import sys
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy import false, true
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate= Migrate(app, db)

# Create a variable for the database path
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres1338@localhost:5432/fyyur'

# Hibernate the warnings in the terminal
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#



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
    start_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # This allows us to print our data in python interactive mode
    def __repr__(self):
      return f'<Shows {self.id} {self.venue_id} {self.artist_id} {self.start_time}>'


# db.create_all()
# # TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

# venue1 = Venues(
#   name='The Musical Hop', 
#   city='San Francisco', 
#   state='CA', 
#   address='1015 Folsom Street', 
#   phone='123-123-1234', 
#   image_link='https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60', 
#   facebook_link='https://www.facebook.com/TheMusicalHop', 
#   website_link='https://www.themusicalhop.com', 
#   genres=['Jazz', 'Reggae', 'Swing', 'Classical', 'Folk'],
#   seeking_talent=True,
#   seeking_description='We are on the lookout for a local artist to play every two weeks. Please call us.'
#   )

# venue2 = Venues(
#   name='The Dueling Pianos Bar', 
#   city='New York', 
#   state='NY', 
#   address='335 Delancey Street', 
#   phone='914-003-1132', 
#   image_link='https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80', 
#   facebook_link='https://www.facebook.com/TheDuelingPianosBar', 
#   website_link='https://www.duelingpianos.com', 
#   genres=['Classical', 'R&B', 'Hip-Hop'],
#   seeking_talent=True,
#   seeking_description='Check us out for more info!'
#   )

# venue3 = Venues(
#   name='Park Square Live Music & Coffee', 
#   city='San Francisco', 
#   state='CA', 
#   address='34 Whiskey Moore Ave', 
#   phone='415-000-1234', 
#   image_link='https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80', 
#   facebook_link='https://www.facebook.com/ParkSquareLiveMusicAndCoffee', 
#   website_link='https://www.parksquarelivemusicandcoffee.com', 
#   genres=['Rock n Roll', 'Jazz', 'Classical', 'Folk'],
#   seeking_talent=True,
#   seeking_description='Hit us up for more info!'
#   )

# db.session.add(venue1)
# db.session.add(venue2)
# db.session.add(venue3)
# db.session.commit()

# artist1= Artists(
#   name='Guns N Petals', 
#   city='San Francisco', 
#   state='CA', 
#   phone='326-123-5000', 
#   genres=['Rock n Roll'], 
#   image_link='https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80', 
#   facebook_link='https://www.facebook.com/GunsNPetals', 
#   website_link='https://www.gunsnpetalsband.com', 
#   seeking_venue=True,
#   seeking_description='Looking for shows to perform at in the San Francisco Bay Area!'
#   )

# artist2 = Artists(
#   name='Matt Quevedo', 
#   city='New York', 
#   state='NY', 
#   phone='300-400-5000', 
#   genres=['Jazz'], 
#   image_link='https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80', 
#   facebook_link='https://www.facebook.com/mattquevedo923251523', 
#   website_link='https://www.mattquevedo.org', 
#   seeking_venue=True,
#   seeking_description='Looking for shows to perform at in the San Francisco Bay Area!'
#   )

# artist3 = Artists(
#   name='The Wild Sax Band', 
#   city='San Francisco', 
#   state='CA', 
#   phone='432-325-5432', 
#   genres=['Jazz', 'Classical'], 
#   image_link='https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80', 
#   facebook_link='https://www.facebook.com/wildsaxband', 
#   website_link='https://www.thewildsaxband.com', 
#   seeking_venue=True,
#   seeking_description='Looking for shows to perform at in the San Francisco Bay Area!'
#   )

# db.session.add(artist1)
# db.session.add(artist2)
# db.session.add(artist3)

# db.session.commit()

# show1 = Shows(
#   artist_id=1,
#   venue_id=1,
#   start_time="2019-05-21T21:30:00.000Z"
#   )

# show2 = Shows(
#   artist_id=3,
#   venue_id=3,
#   start_time="2019-06-15T20:00:00.000Z"
#   )

# show3 = Shows(
#   artist_id=2,
#   venue_id=2,
#   start_time="2019-06-15T23:00:00.000Z"
#   )

# show4 = Shows(
#   artist_id=1,
#   venue_id=3,
#   start_time="2035-04-15T20:00:00.000Z"
#   )

# show5 = Shows(
#   artist_id=2,
#   venue_id=1,
#   start_time="2035-04-15T23:00:00.000Z"
#   )

# db.session.add(show1)
# db.session.add(show2)
# db.session.add(show3)
# db.session.add(show4)
# db.session.add(show5)
# db.session.commit()







#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  # venue_areas = Venues.query.all()
  # data = []

  # for area in venue_areas:
  #   fetched_venues = Venues.query.filter_by(city=area.city).filter_by(state=area.state).order_by(Venues.state)
  #   venue_data = []
  #   for venue in fetched_venues:
  #     venue_data.append({
  #       "id": venue.id,
  #       "name": venue.name, 
  #       # "num_upcoming_shows": len(db.session.query(Shows).filter(Shows.venue_id==1).filter(Shows.start_time>datetime.now()).all())
  #     })
  #   data.append({
  #     "city": area.city,
  #     "state": area.state, 
  #     "venues": venue_data
  #   })

  #Come back to this one

  data = []
  areas = db.session.query(Venues.city, Venues.state, db.func.count(Venues.id)).group_by(Venues.city, Venues.state).all()
  
  
  
  for city, state, venue_count in areas:
      venues = Venues.query.filter(Venues.city == city).all()
      data.append({
          'city': city,
          'state': state,
          'venue_count': venue_count,
          'venues': []
      })

      for venue in venues:
          shows = db.session.query(Shows).filter(Shows.venue_id == venue.id).all()
          past_shows = []
          upcoming_shows = []
          for show in shows:
              if show.start_time > datetime.now():
                  upcoming_shows.append({
                      "artist_id": show.artist_id,
                      "artist_name": show.artist.name,
                      # "artist_image_link": show.artist.image_link,
                      # "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
                  })
              else:
                  past_shows.append({
                      "artist_id": show.artist_id,
                      "artist_name": show.artist.name,
                      # "artist_image_link": show.artist.image_link,
                      # "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
                  })

          data[-1]['venues'].append({
              "id": venue.id,
              "name": venue.name,
              "num_upcoming_shows": len(upcoming_shows),
              "num_past_shows": len(past_shows),
              "upcoming_shows": upcoming_shows,
              "past_shows": past_shows,
              
          })
          
  
  # data=[{
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "venues": [{
  #     "id": 1,
  #     "name": "The Musical Hop",
  #     "num_upcoming_shows": 0,
  #   }, {
  #     "id": 3,
  #     "name": "Park Square Live Music & Coffee",
  #     "num_upcoming_shows": 1,
  #   }]
  # }, {
  #   "city": "New York",
  #   "state": "NY",
  #   "venues": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }]
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')
  search_results = db.session.query(Venues).filter(Venues.name.ilike(f'%{search_term}%')).all()
  data = []

  for result in search_results:
    data.append({
      "id": result.id,
      "name": result.name,
      # "num_upcoming_shows": len(db.session.query(Shows).filter(Shows.venue_id == result.id).filter(Shows.start_time > datetime.now()).all()),
    })
  response={
    "data": data,
    "count": len(search_results)  
  }

  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  venues = Venues.query.get(venue_id)
  # Return a 404 error if the venue is not found
  if not venues: 
    return render_template('errors/404.html')
  #Create the data structure for the template
  upcoming_shows = []
  past_shows = []
  
  #Get the upcoming shows
  upcoming_shows_query = db.session.query(Shows).join(Artists).filter(Shows.venue_id==venue_id).filter(Shows.start_time>datetime.now()).all()
  
  #Get the past shows
  past_shows_query = db.session.query(Shows).join(Artists).filter(Shows.venue_id==venue_id).filter(Shows.start_time<datetime.now()).all()
  
  # Loop through the upcoming shows and add them to the upcoming shows list
  for shows in upcoming_shows_query:
    upcoming_shows.append({
      "artist_id": shows.artist_id,
      "artist_name": shows.artist.name,
      "start_time": shows.start_time.strftime("%Y-%m-%d %H:%M:%S"),
      "artist_image_link": shows.artist.image_link
      
    })

  # Loop through the past shows and add them to the past shows list
  for shows in past_shows_query:
    past_shows.append({
      "artist_id": shows.artist_id,
      "artist_name": shows.artist.name,
      "start_time": shows.start_time.strftime('%Y-%m-%d %H:%M:%S'),
      "artist_image_link": shows.artist.image_link 
    })

 # Get the venue details
  fetched_data = {
    "id": venues.id,
    "name": venues.name,
    "address": venues.address,
    "genres": venues.genres,
    "phone": venues.phone,
    "city": venues.city,
    "state": venues.state,
    "facebook_link": venues.facebook_link,
    "website": venues.website_link,
    "seeking_talent": venues.seeking_talent,
    "seeking_description": venues.seeking_description,
    "image_link": venues.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }

  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  # data1={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #   "past_shows": [{
  #     "artist_id": 4,
  #     "artist_name": "Guns N Petals",
  #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 2,
  #   "name": "The Dueling Pianos Bar",
  #   "genres": ["Classical", "R&B", "Hip-Hop"],
  #   "address": "335 Delancey Street",
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "914-003-1132",
  #   "website": "https://www.theduelingpianos.com",
  #   "facebook_link": "https://www.facebook.com/theduelingpianos",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 3,
  #   "name": "Park Square Live Music & Coffee",
  #   "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
  #   "address": "34 Whiskey Moore Ave",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "415-000-1234",
  #   "website": "https://www.parksquarelivemusicandcoffee.com",
  #   "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #   "past_shows": [{
  #     "artist_id": 5,
  #     "artist_name": "Matt Quevedo",
  #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [{
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 1,
  # }
  data = list(filter(lambda d: d['id'] == venue_id, [fetched_data]))[0]
  return render_template('pages/show_venue.html', venue=data, id=venue_id)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # If there is no error.
  error = False
  
  # Set a boolean to ensure that seeking_talent is not null
  if 'seeking_talent' in request.form:
    talent = True

  else:
    talent = False
  
  
  # Attempt to post the data to the form.
  try: 
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    address = request.form['address']
    phone = request.form['phone']
    genres = request.form.getlist('genres')
    image_link = request.form['image_link']
    facebook_link = request.form['facebook_link']
    website_link = request.form['website_link']
    seeking_talent = talent
    seeking_description = request.form['seeking_description']

    # Insert the data into the database.
    new_venue = Venues(name=name, city=city, state=state, address=address, phone=phone, genres=genres, facebook_link=facebook_link, image_link=image_link, website_link=website_link, seeking_talent=seeking_talent, seeking_description=seeking_description)
    db.session.add(new_venue)
    # Commit the data to the database.
    db.session.commit()

  except: 
    # If there is an error, set the error flag to True.
    error = True
    # Rollback the data to the database.
    db.session.rollback()
    # Print the error message.
    print(sys.exc_info())
  finally: 
    # Close the database session.
    db.session.close()

    # If there is an error, post an error message on the page.
  if error: 
    flash('An error occurred. Venue ' + request.form['name']+ ' could not be listed.')
  # on successful db insert, flash success
  if not error: 
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')



@app.route('/venues/delete/<venue_id>', methods=['GET'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  venue_to_delete = Venues.query.get_or_404(venue_id)
  # shows_to_delete = Shows.query.get(venue_id)
  error = False
  try:
    # db.session.delete(shows_to_delete)
    db.session.delete(venue_to_delete)
    db.session.commit()
    flash("Venue Deleted Successfully. Yay!!! ")
    return render_template('pages/home.html')

  except:
    error = True
    flash("Whoops!!! Venue: " + venue_to_delete.name + " could not be deleted.")
    return render_template('pages/home.html')
  finally: 
    # Close the database session.
    db.session.close()
  
  
  

  
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  # data=[{
  #   "id": 4,
  #   "name": "Guns N Petals",
  # }, {
  #   "id": 5,
  #   "name": "Matt Quevedo",
  # }, {
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  # }]
  
  fetched_artists = Artists.query.all()
  
  data = fetched_artists

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }

  search_term = request.form.get('search_term', '')
  search_result = db.session.query(Artists).filter(Artists.name.ilike(f'%{search_term}%')).all()
  data = []

  for result in search_result:
    upcoming_shows = db.session.query(Shows).filter(Shows.artist_id == result.id).filter(Shows.start_time > datetime.now()).all()
    data.append({
      "id": result.id,
      "name": result.name,
      "num_upcoming_shows": len(upcoming_shows)
    })
  
  response={
    "data": data,
    "count": len(search_result)
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  # data1={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "past_shows": [{
  #     "venue_id": 1,
  #     "venue_name": "The Musical Hop",
  #     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 5,
  #   "name": "Matt Quevedo",
  #   "genres": ["Jazz"],
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "300-400-5000",
  #   "facebook_link": "https://www.facebook.com/mattquevedo923251523",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "past_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  #   "genres": ["Jazz", "Classical"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "432-325-5432",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 3,
  # }

  artist_query = Artists.query.get(artist_id)

  if not artist_query: 
    return render_template('errors/404.html')
  
  # past_shows = []
  # past_shows_query = db.session.query(Shows).join(Venues).filter(Shows.artist_id==artist_id).filter(Shows.start_time<datetime.now()).all()
  
  # for show in past_shows_query:
  #   past_shows.append({
  #     "venue_id": show.venue_id,
  #     "venue_name": show.venue.name,
  #     "artist_image_link": show.venue.image_link,
  #     "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
  #   })
  
  # upcoming_shows = []
  # upcoming_shows_query = db.session.query(Shows).join(Venues).filter(Shows.artist_id==artist_id).filter(Shows.start_time>datetime.now()).all()
  
  # for show in upcoming_shows_query:
  #   upcoming_shows.append({
  #     "venue_id": show.venue_id,
  #     "venue_name": show.venue.name,
  #     "artist_image_link": show.venue.image_link,
  #     "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
  #   })
  
  # print(all_shows)
  all_shows = Shows.query.all()
  for shows in all_shows:
          # venues = db.session.query(Venues).filter(Venues.artist_id == artist_id).all()
    shows = db.session.query(Shows).join(Venues).filter(Shows.artist_id==artist_id).all()
    
    past_shows = []
    upcoming_shows = []
    for show in shows:
      if show.start_time > datetime.now():
        upcoming_shows.append({
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
        })
      else:
        past_shows.append({
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
        })

        

  fetched_data = {
    "id": artist_query.id,
    "name": artist_query.name,
    "genres": artist_query.genres,
    "city": artist_query.city,
    "state": artist_query.state,
    "phone": artist_query.phone,
    "website_link": artist_query.website_link,
    "facebook_link": artist_query.facebook_link,
    "seeking_venue": artist_query.seeking_venue,
    "seeking_description": artist_query.seeking_description,
    "image_link": artist_query.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }


  
  data = list(filter(lambda d: d['id'] == artist_id, [fetched_data]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  fetched_artist_data = db.session.query(Artists).get(artist_id)
  
  if not fetched_artist_data:
    return render_template('errors/404.html')
  else:
    form.name.data = fetched_artist_data.name
    form.city.data = fetched_artist_data.city
    form.state.data = fetched_artist_data.state
    form.phone.data = fetched_artist_data.phone
    form.genres.data = fetched_artist_data.genres
    form.facebook_link.data = fetched_artist_data.facebook_link
    form.image_link.data = fetched_artist_data.image_link
    form.website_link.data = fetched_artist_data.website_link
    form.seeking_venue.data = fetched_artist_data.seeking_venue
    form.seeking_description.data = fetched_artist_data.seeking_description



  # artist={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  # }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=fetched_artist_data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error = False
  
  new_artist_data = db.session.query(Artists).get(artist_id)
  
  try:
    new_artist_data.name = request.form['name']
    new_artist_data.city = request.form['city']
    new_artist_data.state = request.form['state']
    new_artist_data.phone = request.form['phone']
    new_artist_data.genres = request.form.getlist('genres')
    new_artist_data.facebook_link = request.form['facebook_link']
    new_artist_data.image_link = request.form['image_link']
    new_artist_data.website_link = request.form['website_link']
    new_artist_data.seeking_venue = request.form['seeking_venue']
    new_artist_data.seeking_description = request.form['seeking_description']
    

    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(error)
    print(sys.exc_info())
  finally:
    db.session.close()
  
  if error:
    flash('Oh no!. Artist data could not be updated.')
  else:
    flash('Artist data successfully updated!')

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()

  fetched_venue_data = db.session.query(Venues).get(venue_id)

  if not fetched_venue_data:
    return render_template('errors/404.html')

  else:
    form.name.data = fetched_venue_data.name
    form.city.data = fetched_venue_data.city
    form.state.data = fetched_venue_data.state
    form.phone.data = fetched_venue_data.phone
    form.address.data = fetched_venue_data.address
    form.genres.data = fetched_venue_data.genres
    form.facebook_link.data = fetched_venue_data.facebook_link
    form.image_link.data = fetched_venue_data.image_link
    form.website_link.data = fetched_venue_data.website_link
    form.seeking_talent.data = fetched_venue_data.seeking_talent
    form.seeking_description.data = fetched_venue_data.seeking_description


  # venue={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  # }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=fetched_venue_data)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error = False
  new_venue_data = db.session.query(Venues).get(venue_id)

  try:
    new_venue_data.name = request.form['name']
    new_venue_data.city = request.form['city']
    new_venue_data.state = request.form['state']
    new_venue_data.phone = request.form['phone']
    new_venue_data.address = request.form['address']
    new_venue_data.genres = request.form.getlist('genres')
    new_venue_data.facebook_link = request.form['facebook_link']
    new_venue_data.image_link = request.form['image_link']
    new_venue_data.website_link = request.form['website_link']
    new_venue_data.seeking_talent = request.form['seeking_talent']
    new_venue_data.seeking_description = request.form['seeking_description']

    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

  if error:
    flash('Oh no!. Venue data could not be updated.')
  else:
    flash('Venue data successfully updated!')
  
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # error = False
  # try:
  #   new_artist_data = Artists(
  #     name=request.form['name'],
  #     city=request.form['city'],
  #     state=request.form['state'],
  #     phone=request.form['phone'],
  #     genres=request.form.getlist('genres'),
  #     facebook_link=request.form['facebook_link'],
  #     image_link=request.form['image_link'],
  #     website_link=request.form['website_link'],
  #     seeking_venue=request.form['seeking_venue'],
  #     seeking_description=request.form['seeking_description']
  #   )

  #   db.session.add(new_artist_data)
  #   db.session.commit()
  # except:
  #   error = True
  #   db.session.rollback()
  #   print(sys.exc_info())
  # finally:
  #   db.session.close()

  # If there is no error.
  error = False
  
  # Set a boolean to ensure that seeking_talent is not null
  if 'seeking_venue' in request.form:
    venue = True
  else:
    venue = False

  # Attempt to post the data from the form to the db.
  try: 
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    genres = request.form.getlist('genres')
    facebook_link = request.form['facebook_link']
    image_link = request.form['image_link']
    website_link = request.form['website_link']
    seeking_venue = venue
    seeking_description = request.form['seeking_description']

    # Insert the data into the database.
    new_artist = Artists(name=name, city=city, state=state, phone=phone, genres=genres, facebook_link=facebook_link, image_link=image_link, website_link=website_link, seeking_venue=seeking_venue, seeking_description=seeking_description)
    db.session.add(new_artist)
    # Commit the data to the database.
    db.session.commit()

  except: 
    # If there is an error, set the error flag to True.
    error = True
    # Rollback the data to the database.
    db.session.rollback()
    # Print the error message.
    print(sys.exc_info())
  finally: 
    # Close the database session.
    db.session.close()

  if error:
    flash('Oh no!. Artist: ' + request.form['name'] + 'could not be added.')
  else:
    flash('Artist: ' + request.form['name'] + ' was successfully listed!')
  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.

  # Query the database for all the shows, and sort them by the date.
  fetchedShows = Shows.query.order_by(Shows.start_time < datetime.now()).all()
  
  data = []

  for shows in fetchedShows: 
    data.append({
      "venue_id": shows.venue_id,
      "venue_name": shows.venue.name,
      "artist_id": shows.artist_id,
      "artist_name": shows.artist.name, 
      "start_time": shows.start_time.strftime('%Y-%m-%d %H:%M:%S'),
      "artist_image_link": shows.artist.image_link
    })


  # data=[{
  #   "venue_id": 1,
  #   "venue_name": "The Musical Hop",
  #   "artist_id": 4,
  #   "artist_name": "Guns N Petals",
  #   "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "start_time": "2019-05-21T21:30:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 5,
  #   "artist_name": "Matt Quevedo",
  #   "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "start_time": "2019-06-15T23:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-01T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-08T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-15T20:00:00.000Z"
  # }]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  error = False
  try:
    new_show_data = Shows(
      venue_id=request.form['venue_id'],
      artist_id=request.form['artist_id'],
      start_time=request.form['start_time']
    )

    db.session.add(new_show_data)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('Oh no!. Show data could not be added.')
  else:
    flash('Show was successfully listed!')
  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug = True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
