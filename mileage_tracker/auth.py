import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from mileage_tracker.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')
# Creating a Blueprint called 'auth'. __name__ tells bp where it is defined, and url_prefix will be prepended to all URLs
# associated with the blueprint

@bp.route('/register', methods=('GET', 'POST'))
def register():
    # Creating the route for the registration page
    if request.method == 'POST':
        # If a post request is made, setting the variables to the form values
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone_number = request.form['phone_number']
        db = get_db()
        error = None

        # Validating that username and password fields are not empty
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not phone_number:
            error = 'Phone number is required.'
        elif not email:
            error = 'Email is required.'
         
        if error is None:
            try:
                db.execute (
                    "INSERT INTO user (username, password, email, phone_number) VALUES (?, ?, ?, ?)",
                    # .execute takes a SQL query with ? placeholders and a tuple of values to fill the placeholders with
                    (username, generate_password_hash(password), email, phone_number),
                    # This is the tuple, the password is hashed of course
                )
                db.commit() # This is called to save the changes to the database
            except db.IntegrityError: # This error occurs if the username already exists
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))
                # If registration is successful, redirect to login page
            
        flash(error) # Showing an error if one occurs

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    # Creating the route for the login page
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
            # The user is queried and stored in a the variable user
        ).fetchone() # Ensures only one row is grabbed from the table, returns None if no results are found

        if user is None:
            # Checking that the username is there and that 
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('vehicle.index'))
            # Creating a session for the current user, will be used for subsequent requests with a cookie
        
        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    # Function that runs before view function, no matter the URL. Checks if a user id is stored in the session, if yes it gets
    # the user's data from the database, storing it on g.user
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
    # Nothing to display upon logout, just redirecting to login page

def login_required(view):
    # Function to wrap a different view function, will be used to check if the user is loaded, and if not, redirects to login page
    # Useful for views that should only be accessed when you're logged in
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view