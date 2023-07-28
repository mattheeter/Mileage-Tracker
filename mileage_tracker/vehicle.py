from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.exceptions import abort

from mileage_tracker.auth import login_required
from mileage_tracker.db import get_db

bp = Blueprint('vehicle', __name__, url_prefix='/vehicle') # Creating blueprint object

@bp.route('/create', methods=('GET', 'POST'))
@login_required # Login required decorator to make sure user is logged in before they add vehicle(s)
def create():
    # Route for adding vehicles for a user
    if request.method == 'POST':
        # If a post request is made, executing this code
        year = request.form['model_year'] # Pulling parameters from the form request field
        make = request.form['make']
        model = request.form['model']
        miles = request.form['miles']
        error = None

        if not year: # If a field is not filled out
            error = 'Year is required.'
        if not make:
            error = 'Make is required'
        if not model:
            error = 'Model is required'
        if not miles:
            error = 'Mileage is required'

        if error is not None: # If there is an error, display it
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO vehicle (model_year, make, model, owner_id, miles)'
                'VALUES (?, ?, ?, ?, ?)',
                (year, make, model, g.user['id'], miles)
            ) # Inserting values from the form into the db, owner_id is done by the g object
            db.commit()
            return redirect(url_for('vehicle.index')) # Once vehicle has been created, redirecting to index
        
    return render_template('vehicle/create.html')

@bp.route('/')
@login_required
def index():
    # Route where all vehicle stats will be stored
    db = get_db()
    vehicles = db.execute(
        'SELECT v.id, model_year, make, model, miles '
        'FROM vehicle v '
        'JOIN user u ON v.owner_id = u.id ' # Using dot notation and JOIN so that user info is included
        'WHERE v.owner_id = ? ' # Only getting vehicles whose owner_id = g.user['id']
        'ORDER BY created ASC',
        (g.user['id'],) # NEED TO FIX FROM STRING TYPE TO INT -- Fixed, needs comma even though there's only one item
    ).fetchall()
    return render_template('vehicle/index.html', vehicles=vehicles)

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):

    vehicle = get_vehicle(id) # Getting vehicle information to display on the page  

    # Route for updating a vehicle
    if request.method == 'POST':
        # If a post request is made, executing this code
        year = request.form['model_year']
        make = request.form['make']
        model = request.form['model']
        miles = request.form['miles']
        error = None

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE vehicle '
                'SET model_year = ?, make = ?, model = ?, miles = ? '
                'WHERE id = ?',
                (year, make, model, miles, id)
            ) # Changing the updated values
            db.commit()
            return redirect(url_for('vehicle.index')) # Once vehicle has been updated, redirecting to index

    return render_template('vehicle/update.html', vehicle=1)

def get_vehicle(id, check_author=True):
    # Function to retrieve a vehicle from the database to be updated or deleted
    db = get_db()
    vehicle = db.execute( # Fetching vehicle using WHERE to specify what id to get it from
        'SELECT id, model_year, make, model, miles, owner_id '
        'FROM vehicle '
        'WHERE id = ?',
        (id,)
    ).fetchone()

    if vehicle is None:
        # If there is not vehicle for that particular id
        abort(404, f"Vehicle id {id} doesn't exist.")

    if check_author and (vehicle['owner_id'] != g.user['id']):
        # If the vehicle owner_id and the g.user id do not match up
        abort(403)
    
    return vehicle

