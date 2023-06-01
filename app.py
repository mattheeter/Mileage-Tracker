from flask import Flask # Importing the Flask class to create a Flask object
from flask import render_template # render_template used to return html from the routes

app = Flask(__name__) # Creating new Flask object, with the special vairable __name__ used to automatically choose the module name

@app.route('/') # Decorator for "registering" the route
def home(methods=['GET', 'POST']):
    return render_template('home.html')
