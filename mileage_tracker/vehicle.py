from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.exceptions import abort

from mileage_tracker.auth import login_required
from mileage_tracker.db import get_db

bp = Blueprint('vehicle', __name__, url_prefix='/vehicle') # Creating blueprint object (, url_prefix='/vehicle')

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
        'SELECT model_year, make, model, miles '
        'FROM vehicle '
        # 'WHERE owner_id = ?',
        # (g.user['id'])
    ).fetchall()
    return render_template('vehicle/index.html', vehicles=vehicles)

    #  {% if g.user['id'] == post['author_id'] %}
    #     <a class="action" href="{{ url_for('vehicle.update', id=post['id']) }}">Edit</a>
    #   {% endif %}

@bp.route('/update')
@login_required
def update():
    return render_template('base.html')