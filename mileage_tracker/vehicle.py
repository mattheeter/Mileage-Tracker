from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from mileage_tracker.auth import login_required
from mileage_tracker.db import get_db

bp = Blueprint('vehicle', __name__, url_prefix='vehicle') # Creating bluepring object

@bp.route('/create', methods=('GET', 'POST'))
@login_required # Login required decorator to make sure user is logged in before they add vehicle(s)
def create():
    # Route for adding vehicles for a user
    if request.method == 'POST':
        year = request.form['model_year'] # Pulling parameters from the form request field
        make = request.form['make']
        model = request.form['model']
        error = None

        if not year: # If a field is not filled out
            error = 'Year is required.'
        if not make:
            error = 'Make is required'
        if not model:
            error = 'Model is required'

        if error is not None: # If there is an error, display it
            flash(error)
        else:
            db = get_db()
            db.ececute(
                'INSERT INTO vehicle (model_year, make, model, owner_id)',
                'VALUES (?, ?, ?, ?)',
                (year, make, model, g.user['id'])
            ) # Inserting values from the form into the db, owner_id is done by the g object
        
        return render_template('vehicle/create.html')

