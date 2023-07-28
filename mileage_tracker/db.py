import sqlite3

import click
from flask import current_app, g
# g is a special object that changes for each database request. It stores data that might be accessed by multiple functions
# during the request.
# current_app is another special object that points to the Flask application when handling a request. Since we used an
# application factory, there is no application object. 

def get_db():
    # Called when the application has been created and is handling a request
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'], # Establishes a connection to the file pointed at by the DATABASE config key
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row # Telling application to return rows that act like dictionaries

    return g.db


def close_db(e=None):
    # Checks if a connection to the db was created, if so, closing it
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    # get_db returns a database connection, which executes the commmands read from the file

    with current_app.open_resource('schema.sql') as f:
        # Opening a file relative to the mileage_tracker package, useful when later you don't know where the locaion is
        db.executescript(f.read().decode('utf-8'))

@click.command('init-db')
def init_db_command():
    # Clear the existing data and create new tables
    # click.command defines a command line command called init-db that calls the init_db function and shows the message to the user
    init_db()
    click.echo('Initialized the database')
    # Ran the command by typing "flask --app mileage_tracker init-db" to initialize a sqlite database

def init_app(app):
    # init_db and init_db_command functions need to be registered with tthe application instanve, else they won't be 
    # used by the application
    app.teardown_appcontext(close_db)
    # Telling Flask to call the function when cleaning up after returning the response
    app.cli.add_command(init_db_command)
    # Adds a new command with the flask command (similar to when using "flask --app ... run")

# View the database: https://stackoverflow.com/questions/40993895/how-to-see-a-sqlite-database-content-with-visual-studio-code