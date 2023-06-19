from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from mileage_tracker.db import get_db

bp = Blueprint('tracker', __name__)
# New Blueprint to be registered within the factory again

@bp.route('/', methods=('GET', 'POST'))
def tracker():
    db = get_db()
    miles = db.execute(
        'SELECT '
    )