#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
from re import A
import sys
import dateutil.parser
import datetime
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from models import db, Venues, Artists, Shows

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate= Migrate(app, db)


# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
# Moved to models.py


#----------------------------------------------------------------------------#
# # TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.




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

  data = []
  areas = db.session.query(Venues.city, Venues.state, db.func.count(Venues.id)).group_by(Venues.city, Venues.state).all()
    
  for city, state, num_of_venues in areas:
      venues = Venues.query.filter(Venues.city == city).all()
      data.append({
          'city': city,
          'state': state,
          'num_of_venues': num_of_venues,
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
                      "artist_name": show.artist.name
                  })
              else:
                  past_shows.append({
                      "artist_id": show.artist_id,
                      "artist_name": show.artist.name
                  })

          data[-1]['venues'].append({
              "id": venue.id,
              "name": venue.name,
              "num_upcoming_shows": len(upcoming_shows),
              "num_past_shows": len(past_shows),
              "upcoming_shows": upcoming_shows,
              "past_shows": past_shows  
          })
  
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # search for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')
  search_results = db.session.query(Venues).filter(Venues.name.ilike(f'%{search_term}%')).all()
  data = []

  for result in search_results:
    data.append({
      "id": result.id,
      "name": result.name
    })
  response={
    "data": data,
    "count": len(search_results)  
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
 
  # TODO: replace with real venue data from the venues table, using venue_id
  # shows the venue page with the given venue_id
  venues = Venues.query.get_or_404(venue_id)
  
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
  
  # Set a boolean to ensure that seeking_talent is not null
  if 'seeking_talent' in request.form:
    talent = True

  else:
    talent = False
  new = request.form.get
  form = VenueForm(request.form)

  if form.validate():
    try:
      new_venue = Venues( name=new('name'),
                          city=new('city'),
                          state=new('state'), 
                          address=new('address'),
                          phone=new('phone'),
                          genres=request.form.getlist('genres'), 
                          facebook_link=new('facebook_link'),
                          website_link=new('website_link'), 
                          image_link=new('image_link'),
                          seeking_talent=talent, 
                          seeking_description=new('seeking_description')
                        )
  
      db.session.add(new_venue)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
      return render_template('pages/home.html')
    except:
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
      return render_template('pages/home.html')
    finally: 
    # Close the database session.
      db.session.close()
  else:
    for field, message in form.errors.items():
            flash(field + ' - ' + str(message), 'danger')
    return render_template('forms/new_venue.html', form=form)
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  
  

@app.route('/venues/delete/<venue_id>', methods=['GET'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  venue_to_delete = Venues.query.get_or_404(venue_id)
  error = False
  try:
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
  
  fetched_artists = Artists.query.all()
  
  data = fetched_artists

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
 
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
  
  artist_query = Artists.query.get(artist_id)

  if not artist_query: 
    return render_template('errors/404.html')
  
 
  all_shows = Shows.query.all()
  for shows in all_shows:
    shows = db.session.query(Shows).join(Venues).filter(Shows.artist_id==artist_id).all()
    
    past_shows = []
    upcoming_shows = []
    for show in shows:
      if show.start_time > datetime.now():
        upcoming_shows.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "venue_image_link": show.venue.image_link,
            "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
        })
      else:
        past_shows.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "venue_image_link": show.venue.image_link,
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
  # TODO: populate form with fields from artist with ID <artist_id>
  
  form = ArtistForm()
  fetched_artist_data = db.session.query(Artists).get_or_404(artist_id)
  
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

  return render_template('forms/edit_artist.html', form=form, artist=fetched_artist_data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  
  updated_artist = Artists.query.get(artist_id)
  form = ArtistForm(request.form)

  if form.validate():
    updated_artist.name = form.name.data
    updated_artist.city = form.city.data
    updated_artist.state = form.state.data
    updated_artist.phone = form.phone.data
    updated_artist.genres = request.form.getlist('genres')
    updated_artist.facebook_link = form.facebook_link.data
    updated_artist.image_link = form.image_link.data
    updated_artist.website_link = form.website_link.data
    updated_artist.seeking_venue = form.seeking_venue.data
    updated_artist.seeking_description = form.seeking_description.data
    db.session.commit()
    
    flash('Artist data updated Successfully!!!')
    return redirect(url_for('show_artist', artist_id=artist_id))
  else:
    for field, message in form.errors.items():
            flash(field + ' - ' + str(message), 'danger')
    return redirect(url_for('edit_artist', artist_id=artist_id))
  
  
  

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

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=fetched_venue_data)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  updated_venue = Venues.query.get(venue_id)
  form = VenueForm(request.form)

  if form.validate():
    updated_venue.name = form.name.data
    updated_venue.city = form.city.data
    updated_venue.state = form.state.data
    updated_venue.address = form.address.data
    updated_venue.phone = form.phone.data
    updated_venue.genres = request.form.getlist('genres')
    updated_venue.facebook_link = form.facebook_link.data
    updated_venue.image_link = form.image_link.data
    updated_venue.website_link = form.website_link.data
    updated_venue.seeking_talent = form.seeking_talent.data
    updated_venue.seeking_description = form.seeking_description.data
    db.session.commit()
    
    flash('Venue data updated Successfully!!!')
    return redirect(url_for('show_venue', venue_id=venue_id))
  else:
    for field, message in form.errors.items():
            flash(field + ' - ' + str(message), 'danger')
    return redirect(url_for('edit_venue', venue_id=venue_id))
  

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

  # Set a boolean to ensure that seeking_venue is not null
  if 'seeking_venue' in request.form:
    venue = True
  else:
    venue = False
    
  new = request.form.get
    
  form = ArtistForm(request.form)

  if form.validate():
    error = False
    try:
      new_artist = Artists(name=new('name'),
                          city=new('city'),
                          state=new('state'), 
                          phone=new('phone'),
                          genres=request.form.getlist('genres'), 
                          facebook_link=new('facebook_link'),
                          website_link=new('website_link'), 
                          image_link=new('image_link'),
                          seeking_venue=venue, 
                          seeking_description=new('seeking_description')
                        )
  
      db.session.add(new_artist)
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
      return render_template('pages/home.html')
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
      return render_template('pages/home.html')
    finally: 
  #   # Close the database session.
      db.session.close()
  else:
    for field, message in form.errors.items():
            flash(field + ' - ' + str(message), 'danger')
    return render_template('forms/new_artist.html', form=form)
 

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
    flash('Oh no!. Show data could not be added; check the form for errors.')
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
