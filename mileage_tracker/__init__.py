# To run: "flask --app mileage_tracker run --debug"
# To initialize db: flask --app mileage_tracker init-db
import os
from flask import Flask

def create_app(test_config=None):
    # Creating and configuring app, this is known as an application factory
    app = Flask(__name__, instance_relative_config=True)
    # Telling flask that configuration files are stored outside of the Mileage-Tracker Folder
    # Used so that version control does not pick up these files
    app.config.from_mapping(
        SECRET_KEY='dev', # Used to keep data safe, should be set to random string for deployment
        DATABASE=os.path.join(app.instance_path, 'mileage_tracker.sqlite') # Path where database will be stored, in instance folder
    )
    
    if test_config is None:
        # Load instance config (if it exists) when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load config file if passed in
        app.config.from_mapping(test_config)
    
    try: # If no instance directory exists, making one
        os.makedirs(app.instance_path)
    except OSError: # If one does exist, an OSError will be raised, and we know not to make one
        pass
    
    from . import db
    db.init_app(app)
    # Importing and calling function to initialize the database

    from . import auth
    app.register_blueprint(auth.bp)
    # Registering the auth blueprint

    from . import vehicle
    app.register_blueprint(vehicle.bp)
    # Registering the vehicle blueprint

    return app