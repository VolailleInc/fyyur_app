#*****************************************************#
#****************** Library Imports  *****************#
#*****************************************************#

from crypt import methods
import sys
from flask import Flask
from flask import render_template, request, flash, redirect, url_for

import json
import dateutil.parser
import babel
import logging
from logging import Formatter, FileHandler
from forms import *
from models import *


#***** Invoke the Flask Library and assign to app *********#
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)

#********** The function below formats date picks *********#


def date_time_format(value, format='medium'):
    # Let
    date = dateutil.parser.parse(value)
    # Condition
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.date_time_format(date, format)


app.jinja_env.filters['datetime'] = date_time_format


#*****************************************************#
#*********** Controllers Updates Routes **************#
#*****************************************************#


#********************* Home route ********************#
@app.route('/')
def index():
    return render_template('pages/home.html')


pass

#******************* Create Venue route *******************#


@app.route('/venues/create', methods=['GET'])
def create_venues():
    form = Venue_Form()
    return render_template('forms/new_veneu.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submiform():
    error = False
    try:
       venue = Venue_Form()
       venue.name = request.form['name']
       venue.city = request.form['city']
       venue.state = request.form['state']
       venue.address = request.form['address']
       venue.phone = request.form['phone']
       tmp_genres = request.form.getlist('genres')
       venue.genres = ','.join(tmp_genres)
       venue.facebook_link = request.form['facebook_link']
       db.session.add(venue)
       db.session.commit()

    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            flash('There was an error. Venue ' +
                    request.form['name'] + ' Could not be retrieved!')
          else:
              flash('Venue ' + request.form['name'] +
                            ' was successfully retrieved!')
          return render_template('pages/home.html')
        # Query to retrieve all venues
        # venues = Venue_table.query.all()

        # Use set to avoid retrieving duplicate venues
        # locations = set()

        for venue in venues:
            # add city and state records(tuples)
            locations.add((venue.venue_city, venue.venue_state))

        # Loop over each city and state and retrieve venues
        for location in locations:
            data.append({
                "venue_city": location[3],
                "venue_state": location[4],
                "venues": []
            })

        for venue in venues:
            # Set initial coming show to 0
            number_of_coming_shows = 0
            # Retrieve all shows
            shows = Show_table.query.filter_by(venue_id=venue.id).all()
            # get current date to filter number_of_coming_shows
            date_now = datetime.now()
            # Loop through shows
            for show in shows:
                if show.start_time > date_now:
                    number_of_coming_shows += 1

            for venue_location in data:
                if venue.state == venue_location['state'] and venue.city == venue_location['city']:
                    venue_location['venues'].append({
                        "id": venue.id,
                        "name": venue.name,
                        "num_upcoming_shows": number_of_coming_shows
                    })
        return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    result = Venue_table.query.filter(
        Venue_table.name.ilike(f'%{search_term}%'))

    response = {
        "count": result.count(),
        "data": result
    }
    return render_template('pages/search_venues.html', results=response, search_term=search_term)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    venue = Venue_table.query.get(venue_id)
    shows = Show_table.query.filter_by(venue_id=venue_id).all()
    past_shows = []
    upcoming_shows = []
    current_time = datetime.now()

    for show in shows:
        data = {
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": date_time_format(str(show.start_time))
        }
        if show.start_time > current_time:
            upcoming_shows.append(data)
        else:
            past_shows.append(data)

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)
    }

    return render_template('pages/show_venue.html', venue=data)

#***************** Create Venue *******************#


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = Venue_Form()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    try:
        # get form data and create a venue
        form = Venue_Form()
        venue = Venue_table(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            address=form.address.data,
            phone=form.phone.data,
            image_link=form.image_link.data,
            genres=form.genres.data,
            facebook_link=form.facebook_link.data,
            seeking_description=form.seeking_description.data,
            website=form.website.data,
            seeking_talent=form.seeking_talent.data)

        # commit session to database
        db.session.add(venue)
        db.session.commit()

        # flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        # catches errors
        db.session.rollback()
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed.')
    finally:
        # closes session
        db.session.close()
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        # Get venue by ID
        venue = Venue_table.query.get(venue_id)
        venue_name = venue.name

        db.session.delete(venue)
        db.session.commit()

        flash('Venue ' + venue_name + ' was deleted')
    except:
        flash('an error occured and Venue ' + venue_name + ' was not deleted')
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('index'))

#**********************  Artists **********************#


@app.route('/artists')
def artists():
    data = []

    artists = Artist_table.query.all()

    for artist in artists:
        data.append({
            "id": artist.id,
            "name": artist.name
        })
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term', '')

    # Case insensitive search by filter of artists
    result = Artist_table.query.filter(
        Artist_table.name.ilike(f'%{search_term}%'))

    response = {
        "count": result.count(),
        "data": result
    }

    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist_table.query.get(artist_id)
    shows = Show_table.query.filter_by(artist_id=artist_id).all()
    past_shows = []
    upcoming_shows = []
    current_time = datetime.now()

    # Filter shows by upcoming and past shows
    for show in shows:
        data = {
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "venue_image_link": show.venue.image_link,
            "start_time": date_time_format(str(show.start_time))
        }
        if show.start_time > current_time:
            upcoming_shows.append(data)
        else:
            past_shows.append(data)

    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "facebook_link": artist.facebook_link,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)
    }

    return render_template('pages/show_artist.html', artist=data)

#*****************************************************#
#************* Record Updates Routes *****************#
#*****************************************************#


#************* Artist updates routes *****************#
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = Artist_Form()

    artist = Artist_table.query.get(artist_id)

    artist_data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "facebook_link": artist.facebook_link,
        "image_link": artist.image_link
    }

    return render_template('forms/edit_artist.html', form=form, artist=artist_data)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    try:
        form = Artist_Form()

        artist = Artist_table.query.get(artist_id)

        artist.name = form.name.data
        artist.phone = form.phone.data
        artist.state = form.state.data
        artist.city = form.city.data
        artist.genres = form.genres.data
        artist.image_link = form.image_link.data
        artist.facebook_link = form.facebook_link.data

        db.session.commit()
        flash(request.form['name'] + ' Record has been successfully updated!')
    except:
        db.session.rolback()
        flash('An Error has occured and the update unsuccessful')
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = Venue_Form()
    venue = Venue_table.query.get(venue_id)
    venue = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
    }

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    try:
        form = Venue_Form()
        venue = Venue_table.query.get(venue_id)
        name = form.venue_name.data

        venue.name = name
        venue.genres = form.genres.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.address = form.address.data
        venue.phone = form.phone.data
        venue.facebook_link = form.facebook_link.data
        venue.website = form.website.data
        venue.image_link = form.image_link.data
        venue.seeking_talent = form.seeking_talent.data
        venue.seeking_description = form.seeking_description.data

        db.session.commit()
        flash('Venue ' + name + ' has been updated')
    except:
        db.session.rollback()
        flash('An error occured while trying to update Venue')
    finally:
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))

#******************* Create Artist ********************#


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = Artist_Form()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    try:
        form = Artist_Form()
        artist = Artist_table(name=form.artist_name.data, city=form.artist_city.data, state=form.artist_state.data,
                              phone=form.artist_phone.data, genres=form.artist_genres.data,
                              image_link=form.artist_image_link.data, facebook_link=form.artist_facebook_link.data)

        db.session.add(artist)
        db.session.commit()

        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be listed.')
    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.route('/artist/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    try:

        artist = Artist_table.query.get(artist_id)
        artist_name = artist.name

        db.session.delete(artist)
        db.session.commit()

        flash('Artist ' + artist_name + ' was deleted')
    except:
        flash('an error occured and Artist ' +
              artist_name + ' was not deleted')
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('index'))

#********************  Shows ***********************#


@app.route('/shows')
def shows():
    shows = Show_table.query.order_by(db.desc(Show_table.start_time))

    data = []

    for show in shows:
        data.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": date_time_format(str(show.start_time))
        })

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form
    form = Show_Form()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    try:
        show = Show_Form(artist_id=request.form['artist_id'], venue_id=request.form['venue_id'],
                         start_time=request.form['start_time'])

        db.session.add(show)
        db.session.commit()

        flash('Show was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. Show could not be listed.')
    finally:
        db.session.close()

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
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
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
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
